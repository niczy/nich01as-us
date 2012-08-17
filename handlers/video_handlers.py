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
        channel = data_source.get_channel(channel_id)
        offset, limit = handlers.parse_offset_and_limit(self)
        videos = data_source.get_videos_in_channel(channel_id, offset = offset, limit = limit) 
        ret = {}
        ret["channel"] = channel.to_dict()
        ret["videos"] = models.to_dict_array(videos)
        ret["offset"] = offset
        ret["limit"] = limit
        self.render_dict_as_json(ret)

class ChannelPageHandler(handlers.BasePageHandler):
    '''
    Return the chanel information as well as the video list.
    '''
    def get(self, channel_id):
        channel = data_source.get_channel(channel_id)
        offset, limit = handlers.parse_offset_and_limit(self)
        videos = data_source.get_videos_in_channel(channel_id, offset = offset, limit = limit) 
        ret = {}
        ret["channel"] = channel
        ret["videos"] = videos 
        ret["offset"] = offset
        ret["limit"] = limit
        self.render("ChannelListPage.html", ret)

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
            video.do_like()
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
            video.do_dislike()
            video.put()
            self.render_dict_as_json(video.to_dict())

    def get(self):
        if configs.DEBUG:
            return self.post()
