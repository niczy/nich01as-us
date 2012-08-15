import webapp2
import handlers
import handlers
from configs import router_path
from models.VideoModels import ChannelModel 
from models.VideoModels import VideoModel 
import logging
from models import DataSource as data_source

class AdminHomeHandler(handlers.BasePageHandler):
    def get(self):
        self.render("AdminHome.html")

class ChannelUpdateHandler(handlers.BasePageHandler):
    def get(self):
        channel_id = self.request.get("channel_id")
        values = {}

        if channel_id:
            videos = data_source.get_videos_in_channel(channel_id)
            channel = data_source.get_channel(channel_id)
            if channel:
                values["channel"] = channel
            if videos:
                values["videos"] = videos
        self.render("ChannelUpdate.html", values)

    def post(self):
        channel_id = self.request.get("channel_id")
        title = self.request.get("title")
        cover_img = self.request.get("cover_img")
        channel = data_source.get_channel(channel_id)
        if channel:
            self.response.out.write("exist")
        else:
            channel = ChannelModel(key_name = channel_id, title = title, cover_img = cover_img)
            channel.put()
            self.redirect(router_path["admin_channel_list"])




class VideoUpdateHandler(handlers.BasePageHandler):
    def get(self):
        channel_id = self.request.get("channel_id")
        video_id = self.request.get("video_id")
        video = data_source.get_video(channel_id, video_id)
        values = {}
        if channel_id:
            values["channel_id"] = channel_id
        if video:
            values["video"] = video
        self.render("VideoUpdate.html", values)

    def post(self):
        channel_id = self.request.get("channel_id")
        video_id = self.request.get("video_id")
        channel = data_source.get_channel(channel_id)
        video = data_source.get_video(channel_id, video_id)
        if channel:
            title = self.request.get("title")
            cover_img = self.request.get("cover_img")
            video_url = self.request.get("video_url")
            if not video:
                video = VideoModel(parent = channel, title = title, cover_img = cover_img, video_url = video_url)
            else:
                video.title = title
                video.cover_img = cover_img
                video.video_url = video_url
            video.put()
            self.redirect(router_path["admin_channel_update"] + "?channel_id=%s" % (channel_id))
            return self.get()
        else:
            self.response.out.write("channel not exist")


class ParserManageHandler(handlers.BasePageHandler):
    def get(self):
        name = self.request.get("name")
        if name == "youku_girls":
            from tools import youku_parser
            for i in xrange(10):
                video_infos = youku_parser.parse_url("http://www.youku.com/v_showlist/t2c86g0d3p%d.html" % (i))
                for video_info in video_infos:
                    if not data_source.get_video_by_external_id(video_info["source"], video_info["external_id"]):
                        video = data_source.create_video_from_dict("girls", video_info)
                        video.put()
        self.render("ParserManage.html")

