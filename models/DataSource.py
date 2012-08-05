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

def get_videos_in_channel(channel_id, offset = 0, limit = 16):
    key = channel_key(channel_id)
    q = VideoModel.all()
    q.ancestor(key)
    return q.fetch(limit, offset = offset)
