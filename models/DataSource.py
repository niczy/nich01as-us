from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from google.appengine.ext import db


def channel_key(channel_id):
    return db.Key.from_path("ChannelModel", channel_id)

def get_channel(channel_id):
    if not channel_id:
        return None
    return db.get(channel_key(channel_id))

def get_video(channel_id, video_id):
    if channel_id and video_id:
        video_key = db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))
        video = db.get(video_key)
        return video
    return None

def get_video_by_external_id(source, external_id):
    q = VideoModel.all()
    q.filter("external_id =", external_id)
    q.filter("source =", source)
    result = q.fetch(1)
    if result:
        return result[0]
    return None

def get_videos_in_channel(channel_id, offset = 0, limit = 16):
    key = channel_key(channel_id)
    q = VideoModel.all()
    q.ancestor(key)
    q.order("-final_socre")
    return q.fetch(limit, offset = offset)

def create_video_from_dict(channel_id, video_info):
    channel = get_channel(channel_id)
    if not channel:
        raise ValueError("Channel %s not exist" %s (channel_id))
    video = VideoModel(parent = channel, title = video_info["title"], 
            cover_img = video_info["cover_img"], video_url = video_info["video_url"], 
            source = video_info["source"], external_id = video_info["external_id"])

    return video


