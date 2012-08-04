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
    video_key = db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))
    video = db.get(video_key)
    return video
