from google.appengine.ext import db


class ClientFile(db.Model):
    pathname = db.StringProperty()
    platform = db.StringProperty()
    version = db.IntegerProperty()
    content = db.TextProperty()

class ClientVersion(db.Model):
    version = db.IntegerProperty()
    platform = db.StringProperty()
    url = db.StringProperty()
