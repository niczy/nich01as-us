import webapp2
import handlers
import handlers
from models import DataSource as data_source

class AdminHomeHandler(handlers.BasePageHandler):
    def get(self):
        self.render("AdminHome.html")

class ChannelUpdateHandler(handlers.BasePageHandler):
    def get(self):
        channel_id = self.request.get("channel_id")
        channel = data_source.get_channel(channel_id)
        values = {}
        if channel:
            values["channel"] = channel
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
            return self.get()



