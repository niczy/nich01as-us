import webapp2
import handlers
from handlers import BasePageHandler
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from google.appengine.ext import db
import models
import json
from StringIO import StringIO

def channel_key(channel_id):
    return db.Key.from_path("ChannelModel", channel_id)

class ChannelManageHandler(BasePageHandler):
    def get(self):
        self.render("ChannelManage.html")

    def post(self):
        channel_id = self.request.get("channel_id")
        title = self.request.get("title")
        cover_img = self.request.get("cover_img")
        key = channel_key(channel_id)
        if db.get(key):
            self.response.out.write("exist")
        else:
            channel = ChannelModel(key_name = channel_id, title = title, cover_img = cover_img)
            channel.put()
            return self.get()

class ChannelHandler(handlers.BaseJsonHandler):
    def get(self, channel_id):
        key = channel_key(channel_id);
        channel = db.get(key)
        q = VideoModel.all()
        q.ancestor(key)
        videos = q.fetch(10)
        ret = {}
        ret["channel"] = channel.to_dict()
        ret["videos"] = models.to_dict_array(videos)
        self.render_dict_as_json(ret)


class VideoHandler(handlers.BaseJsonHandler):
    def get(self, channel_id, video_id):
        video_key = db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))
        video = db.get(video_key) 
        if video:
            self.render_dict_as_json(video.to_dict())
        else:
            self.response.out.write("{}") 


class VideoManageHandler(BasePageHandler):
    def get(self):
        self.render("VideoManage.html")

    def post(self):
        channel_id = self.request.get("channel_id")
        parent_key = channel_key(channel_id)
        if db.get(parent_key):
            title = self.request.get("title")
            cover_img = self.request.get("cover_img")
            video_url = self.request.get("video_url")
            video = VideoModel(parent = parent_key, title = title, cover_img = cover_img, video_url = video_url)
            video.put()
            return self.get()
        else:
            self.response.out.write("channel not exist")


