'''
Created on Aug 19, 2012

@author: charliezhang
'''

from google.appengine.ext import db

class CommentModel(db.Model):
    comment = db.StringProperty(required=True)
    user = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    parent_id = db.IntegerProperty()
    channel_id = db.StringProperty()
    video_id = db.StringProperty()
    like = db.IntegerProperty()
    dislike = db.IntegerProperty()
    
    def to_dict(self):
        return {"i": self.key().id(),
                "c": self.comment, # comment
                "u": self.user,  # user
                "p": self.parent_id, # parent comment id
                "d": self.dislike, # num dislike
                "l": self.like, #num like
                "ch": self.channel_id,
                "v": self.video_id,
                }