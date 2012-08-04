import webapp2
import handlers
from handlers import BasePageHandler
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from google.appengine.ext import db
import models
import json
from StringIO import StringIO
import models.DataSource as data_source
import configs

def channel_key(channel_id):
    return db.Key.from_path("ChannelModel", channel_id)

class ChannelUpdateHandler(BasePageHandler):
    def get(self):
        self.render("ChannelUpdate.html")

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

class ChannelListHandler(handlers.BasePageHandler):
    def get(self):
        q = ChannelModel.all()
        offset, limit = handlers.parse_offset_and_limit(self)
        values = {}
        channels = q.fetch(limit, offset = offset)
        values["offset"] = offset
        values["limit"] = limit
        values["channels"] = channels
        self.render("ChannelList.html", values)

class ChannelHandler(handlers.BaseJsonHandler):
    '''
    Return the chanel information as well as the video list.
    '''
    def get(self, channel_id):
        key = channel_key(channel_id);
        channel = db.get(key)
        q = VideoModel.all()
        q.ancestor(key)
        offset, limit = handlers.parse_offset_and_limit(self)
        videos = q.fetch(limit, offset = offset)
        ret = {}
        ret["channel"] = channel.to_dict()
        ret["videos"] = models.to_dict_array(videos)
        self.render_dict_as_json(ret)


class VideoHandler(handlers.BaseJsonHandler):
    '''
    Return the detail meta info of a video.
    It requires both channel and video id to specify a video.
    '''
    def get(self, channel_id, video_id):
        video = data_source.get_video(channel_id, video_id)
        if video:
            self.render_dict_as_json(video.to_dict())
        else:
            self.response.out.write("{}") 

class VideoLikeHandler(handlers.BaseJsonHandler):
    '''
    To like a video
    '''
    def post(self):
        channel_id = self.request.get("channel_id")
        video_id = self.request.get("video_id")
        video = data_source.get_video(channel_id, video_id)
        if video:
            video.like = video.like + 1
            video.put()
            self.render_dict_as_json(video.to_dict())
        else:
            self.render_dict_as_json({"error" : "Video not found channel_id=%s, video_id=%s" % (channel_id, video_id)})

    def get(self):
        if configs.DEBUG:
            return self.post()

class VideoDislikeHandler(handlers.BaseJsonHandler):
    '''
    To dislike a video
    '''
    def post(self):
        channel_id = self.request.get("channel_id")
        video_id = int(self.request.get("video_id"))
        video = data_source.get_video(channel_id, video_id)
        if video:
            video.dislike = video.dislike + 1
            video.put()
            self.render_dict_as_json(video.to_dict())

    def get(self):
        if configs.DEBUG:
            return self.post()


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


