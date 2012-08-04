from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from google.appengine.ext import db



def get_video(channel_id, video_id):
    video_key = db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))
    video = db.get(video_key)
    return video
