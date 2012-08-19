from google.appengine.ext import db
import models
from tools.sort import hot

class ChannelModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()

    def to_dict(self):
        ret = models.to_dict(self)
        ret["channel_id"] = self.key().name()
        q = VideoModel.all()
        q.ancestor(self)
        ret["total"] = q.count()
        return ret

class VideoModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()
    video_url = db.StringProperty()
    like = db.IntegerProperty(default = 0)
    dislike = db.IntegerProperty(default = 0)
    editor_score = db.IntegerProperty(default = 0)
    final_score = db.FloatProperty(default = 0.0)
    source = db.StringProperty(default = "")
    external_id = db.StringProperty(default = "")
    created_datetime = db.DateTimeProperty(auto_now_add = True)
    modified_datetime = db.DateTimeProperty(auto_now = True)

    def calculate_score(self):
        self.final_score = hot(self.like, self.dislike, self.created_datetime) + self.editor_score

    def do_like(self):
        self.like += 1
        self.calculate_score()

    def do_dislike(self):
        self.dislike += 1
        self.calculate_score()

    def to_dict(self):
        ret = models.to_dict(self)
        ret["video_id"] = self.key().id()
        ret["channel_id"] = self.parent().key().name()
        return ret;




