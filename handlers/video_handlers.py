import webapp2
import handlers
from handlers import BasePageHandler
from handlers import require_login
from index.indexes import ChannelIndex
from index.indexes import VideoIndex
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from google.appengine.ext import db
import models
import json
import logging
from StringIO import StringIO
import models.DataSource as data_source
import configs
from libs.benchmark import Worktime

class ChannelListHandler(handlers.BasePageHandler):
    @Worktime('ChannelList.Get')
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
    Return the channel information as well as the video list.
    '''
    @Worktime('Channel.Get')
    def get(self, channel_id):
        channel = data_source.get_channel(channel_id)
        offset, limit = handlers.parse_offset_and_limit(self)
        videos = data_source.get_videos_in_channel(channel_id, offset = offset, limit = limit) 
        ret = {}
        ret["channel"] = channel.to_dict()
        ret["videos"] = videos
        ret["offset"] = offset
        ret["limit"] = limit
        self.render_dict_as_json(ret)

class ChannelPageHandler(handlers.BasePageHandler):
    '''
    Return the channel information as well as the video list.
    '''
    @require_login()
    @Worktime('ChannelPage.Get')
    def get(self, channel_id, video_id = '', comment_id = ''):
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
    @Worktime('Video.Get')
    def get(self, channel_id, video_id):
        video = data_source.get_video(channel_id, video_id)
        if video:
            self.render_dict_as_json(video)
        else:
            self.response.out.write("{}") 

class VideoPageHandler(handlers.BasePageHandler):

    @require_login()
    @Worktime('VideoPage.Get')
    def get(self, channel_id, video_id, comment_id=''):
        data_source.view_video(channel_id, video_id)
        self.render("ChannelListPage.html")

class VideoLikeHandler(handlers.BaseJsonHandler):
    '''
    To like a video
    '''
    @require_login()
    def post(self):
        channel_id = self.request.get("channel_id")
        video_id = self.request.get("video_id")   
        video = data_source.get_video(channel_id, video_id)
        key = self.user
        if not key: key = self.request.remote_addr
        if video:
            data_source.like_video(key, channel_id, video_id)
            video["like"] += 1
            self.render_dict_as_json(video)
        else:
            self.render_dict_as_json({"error" : "Video not found channel_id=%s, video_id=%s" % (channel_id, video_id)})

    def get(self):
        if configs.DEBUG:
            return self.post()

class VideoDislikeHandler(handlers.BaseJsonHandler):
    '''
    To dislike a video
    '''
    @require_login()
    def post(self):
        channel_id = self.request.get("channel_id")
        video_id = int(self.request.get("video_id"))
        video = data_source.get_video(channel_id, video_id)
        key = self.user
        if not key: key = self.request.remote_addr
        if video:
            data_source.dislike_video(key, channel_id, video_id)
            video["dislike"] += 1
            self.render_dict_as_json(video)

    def get(self):
        if configs.DEBUG:
            return self.post()
