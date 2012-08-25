'''
Created on Aug 19, 2012

@author: charliezhang
'''

from google.appengine.ext import db

def comment_like_counter(channel_id, video_id, comment_id):
    return "CommentLikeCounter#%s#%s#%s" % (channel_id, video_id, comment_id)

def comment_dislike_counter(channel_id, video_id, comment_id):
    return "CommentDislikeCounter#%s#%s#%s" % (channel_id, video_id, comment_id)

class CommentModel(db.Model):
    comment = db.StringProperty(required=True)
    user = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    parent_id = db.IntegerProperty()

    def to_dict(self):
        return {"i": self.key().id(), # Id
                "c": self.comment, # Comment
                "u": self.user,  # User
                "p": self.parent_id, # Parent comment id
                't': self.created.strftime("%Y%m%d-%H%S%M"), # Time created
                }