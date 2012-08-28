from models import VideoModels
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from models.VideoModels import video_like_counter
from models.VideoModels import video_like_history_counter
from models.VideoModels import video_dislike_counter
from models.VideoModels import video_dislike_history_counter
from models.VideoModels import video_comment_counter
from models.VideoModels import video_view_counter
from models.CommentModels import CommentModel
from models.CommentModels import comment_like_counter
from models.CommentModels import comment_dislike_counter
from google.appengine.ext import db
from libs.cache import Cached
from libs.comment_tree import CommentTree
from libs import fastcounter
import models
import types
import logging

COMMENT_TREE_MAX_SIZE = 10000
COMMENT_TREE_CACHE_SECONDS = 5
CHANNEL_VIDEOS_CACHE_SECONDS = 3600
MAX_CHANNEL_SIZE = 1000
GET_VIDEO_CACHE_SECONDS = 100

COUNTER_UPDATE_SECONDS = 1

def get_channel(channel_id):
    if not channel_id:
        return None
    return db.get(_channel_key(channel_id))

def get_video_model(channel_id, video_id):
    if channel_id and video_id:
        video_key = db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))
        video = db.get(video_key)
        return video
    return None

@Cached(GET_VIDEO_CACHE_SECONDS)
def get_video(channel_id, video_id):
    if channel_id and video_id:
        video = get_video_model(channel_id, video_id).to_dict()
        _populate_video_counters(video)
        return video
    return None

def view_video(channel_id, video_id):
    fastcounter.incr(video_view_counter(channel_id, video_id),
                     1,
                     COUNTER_UPDATE_SECONDS)
    
def like_video(key, channel_id, video_id, delta=1):
    history = video_like_history_counter(key, channel_id, video_id)
    if fastcounter.get_count(history) > 0:
        return
    fastcounter.incr(history, 1, 99999999)
    fastcounter.incr(video_like_counter(channel_id, video_id),
                     delta,
                     COUNTER_UPDATE_SECONDS)
 
def dislike_video(key, channel_id, video_id, delta=1):
    history = video_dislike_history_counter(key, channel_id, video_id)
    if fastcounter.get_count(history) > 0:
        return
    fastcounter.incr(history, 1, 99999999)
    fastcounter.incr(video_dislike_counter(channel_id, video_id),
                     delta,
                     COUNTER_UPDATE_SECONDS)

def get_video_by_external_id(source, external_id):
    q = VideoModel.all()
    q.filter("external_id =", external_id)
    q.filter("source =", source)
    result = q.fetch(1)
    if result:
        return result[0]
    return None

@Cached(CHANNEL_VIDEOS_CACHE_SECONDS)
def get_videos_model_in_channel(channel_id, offset = 0, limit = 16):
    key = _channel_key(channel_id)
    q = VideoModel.all()
    q.ancestor(key)
    q.order("-editor_score")
    return q.fetch(limit, offset = offset)

def get_videos_in_channel(channel_id, offset = 0, limit = 16):
    videos = get_videos_model_in_channel(channel_id, 0, MAX_CHANNEL_SIZE)
    videos = models.to_dict_array(videos)
    _populate_video_counters(videos)
    videos = _score_videos(videos)
    return videos[offset:offset+limit]

def create_video_from_dict(channel_id, video_info):
    channel = get_channel(channel_id)
    if not channel:
        raise ValueError("Channel %s not exist" % (channel_id))
    video = VideoModel(parent = channel, title = video_info["title"], 
            cover_img = video_info["cover_img"], video_url = video_info["video_url"], 
            source = video_info["source"], external_id = video_info["external_id"])

    return video
    
@Cached(COMMENT_TREE_CACHE_SECONDS)
def get_comment_tree(channel_id, video_id, cid, max_num_comments=100):
    tree = _build_comment_tree(channel_id, video_id)
    return tree.get_sub_tree(cid, max_num_comments)

def add_comment(comment, user, channel_id, video_id, parent_id):
    if not user or not channel_id or not video_id:
        return None
    video = _video_key(channel_id, video_id)
    comment = CommentModel(parent = video,
                           comment = comment,
                           user = user,
                           channel_id = channel_id,
                           video_id = video_id,
                           parent_id = int(parent_id))
    comment.put()
    fastcounter.incr(video_comment_counter(channel_id, video_id),
                     1,
                     COUNTER_UPDATE_SECONDS)
    return comment

def dislike_comment(channel_id, video_id, comment_id, delta=1):
    fastcounter.incr(comment_dislike_counter(channel_id, video_id, comment_id),
                     delta,
                     COUNTER_UPDATE_SECONDS)

def like_comment(channel_id, video_id, comment_id, delta=1):
    fastcounter.incr(comment_like_counter(channel_id, video_id, comment_id),
                     delta,
                     COUNTER_UPDATE_SECONDS)

""" *************************************
******* Public functions above **********
************************************* """

def _channel_key(channel_id):
    return db.Key.from_path("ChannelModel", channel_id)

def _video_key(channel_id, video_id):
    return db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))

def _comment_key(channel_id, video_id, comment_id):
    return db.Key.from_path("ChannelModel", channel_id,
                            "VideoModel", int(video_id), "CommentModel", int(comment_id))

@Cached(COMMENT_TREE_CACHE_SECONDS)
def _build_comment_tree(channel_id, video_id):
    video = _video_key(channel_id, video_id)
    q = CommentModel.all()
    q.ancestor(video)
    comments = q.fetch(COMMENT_TREE_MAX_SIZE)
    tree = CommentTree(comments)
    _populate_comment_counters(channel_id, video_id, tree)
    return tree

def _populate_comment_counters(channel_id, video_id, tree):
    counters = []
    like_ctr_to_node = {}
    dislike_ctr_to_node = {}
    for comment in tree.comments():
        like_ctr = comment_like_counter(channel_id, video_id, comment['i'])
        dislike_ctr = comment_dislike_counter(channel_id, video_id, comment['i'])
        counters.extend([like_ctr, dislike_ctr])
        like_ctr_to_node[like_ctr] = comment
        dislike_ctr_to_node[dislike_ctr] = comment
    results = fastcounter.get_counts(counters)
    for i in xrange(0, len(counters)):
        if like_ctr_to_node.has_key(counters[i]):
            node = like_ctr_to_node[counters[i]]
            node['l'] = results[i]
        else:
            node = dislike_ctr_to_node[counters[i]]
            node['d'] = results[i]

def _populate_video_counters(videos):
    if not isinstance(videos, types.ListType):
        videos = [videos]
    counters = []
    cnt_to_video = {}
    for video in videos:
        counters_map = VideoModels.counters_map(video)
        for (k, v) in counters_map.iteritems():
            counters.append(k)
            cnt_to_video[k] = video
    results = fastcounter.get_counts(counters)
    for i in xrange(0, len(counters)):
        cntr = counters[i]
        video = cnt_to_video[cntr]
        counters_map = VideoModels.counters_map(video)
        video[counters_map[cntr]] = results[i]

def _score_videos(videos):
    for v in videos:
        v["final_score"] = VideoModels.score(v)
    return sorted(videos, key=lambda video: -video["final_score"])
