from google.appengine.ext import db

class ChannelModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()

class VideoModel(db.Model):
    title = db.StringProperty()
    cover_img = db.StringProperty()
    video_url = db.StringProperty()


