from google.appengine.ext import db
import models
from tools.sort import hot
from tools.sort import hot2
import logging

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
    
def video_like_counter(channel_id, video_id):
    return "VideoLikeCounter#%s#%s" % (channel_id, video_id)

def video_dislike_counter(channel_id, video_id):
    return "VideoDislikeCounter#%s#%s" % (channel_id, video_id)

def video_view_counter(channel_id, video_id):
    return "VideoViewCounter#%s#%s" % (channel_id, video_id)

def video_comment_counter(channel_id, video_id):
    return "VideoCommentCounter#%s#%s" % (channel_id, video_id)

def counters_map(video):
    key = _counter_key(video)
    return {"VideoLikeCounter%s" % key: "like",
            "VideoDislikeCounter%s" % key: "dislike",
            "VideoViewCounter%s" % key: "view",
            "VideoCommentCounter%s" % key: "comment"}

def score(video):
    return hot2(video["like"], video["dislike"],  video["view"], video["comment"], video["quality_score"], video["created_datetime"])
    
def _counter_key(video):
    return "#%s#%d" % (video["channel_id"], video["video_id"])
    
class VideoModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()
    video_url = db.StringProperty()
    editor_score = db.IntegerProperty(default = 0)
    quality_score = db.FloatProperty(default = 0.0)
    source = db.StringProperty(default = "")
    external_id = db.StringProperty(default = "")
    created_datetime = db.DateTimeProperty(auto_now_add = True)
    modified_datetime = db.DateTimeProperty(auto_now = True)

    def calculate_score(self):
        self.quality_score = 0.0 + self.editor_score
        #self.final_score = hot(self.like, self.dislike, self.created_datetime) + self.editor_score

    def to_dict(self):
        ret = models.to_dict(self)
        ret["video_id"] = self.key().id()
        ret["channel_id"] = self.parent().key().name()
        return ret;
        
    


