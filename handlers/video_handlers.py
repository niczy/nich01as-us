import webapp2
from handlers import BasePageHandler
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from google.appengine.ext import db

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

class ChannelHandler(webapp2.RequestHandler):
    def get(self, channel_id):
        key = channel_key(channel_id);
        channel = db.get(key)
        q = VideoModel.all()
        q.ancestor(key)
        videos = q.fetch(10)
        self.response.out.write("%s %s" % (channel.title, channel.cover_img))
        for video in videos:
            self.response.out.write("video title: %s, video_id: %s" % (video.title, video.key().id()))


class VideoHandler(webapp2.RequestHandler):
    def get(self, channel_id, video_id):
        video_key = db.Key.from_path("ChannelModel", channel_id, "VideoModel", int(video_id))
        video = db.get(video_key) 
        if video:
            self.response.out.write("%s %s" % (video.title, video.video_url))
        else:
            self.response.out.write("not found video: %s" % (video_id))


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


