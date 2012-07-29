from google.appengine.ext import db
import models

class ChannelModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()

    def to_dict(self):
        ret = models.to_dict(self)
        ret["channel_id"] = self.key().name()
        return ret

class VideoModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()
    video_url = db.StringProperty()

    def to_dict(self):
        ret = models.to_dict(self)
        ret["video_id"] = self.key().id()
        ret["channel_id"] = self.parent().key().name()
        return ret;


