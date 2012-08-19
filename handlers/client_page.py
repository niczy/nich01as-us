import webapp2
import jinja2
from handlers import BasePageHandler
from handlers import require_login
from models.ClientModels import ClientFile 
from models.ClientModels import ClientVersion
from models.UserModels import signup
from models.UserModels import signin
from models.UserModels import set_login
from google.appengine.ext import db

def client_file_key_name(platform, version, pathname):
    return "platform %s:version %d:pathname: %s" % (platform, version, pathname)

def client_file_key(platform, version, pathname):
    return db.Key.from_path("ClientFile", client_file_key_name(platform, version, pathname))


class VersionQueryHandler(webapp2.RequestHandler):
    def get(self):
        pathname = self.request.get("pathname")
        platform = self.request.get("platform")
        if pathname:
            q = ClientFile.all()
            q.filter("platform =", platform)
            q.filter("pathname =", pathname)
            q.order("-version")
            f = q.fetch(1)
            if len(f) == 0:
                self.response.out.write(-1)
            else:
                self.response.out.write(f[0].version)
        else:
            q = ClientVersion.all()
            q.filter("platform =", platform)
            q.order("-version")
            f = q.fetch(1)
            if len(f) == 0:
                self.response.out.write("-1")
            else:
                self.response.out.write('{"version":%s, "url": "%s"}' % (f[0].version, f[0].url))
            


class PageContentHandler(webapp2.RequestHandler):
    def get(self):
        platform = self.request.get("platform")
        version = int(self.request.get("version"))
        pathname = self.request.get("pathname")
        clientfile = ClientFile.get(client_file_key(platform, version, pathname))
        self.response.headers["Content-type"] = "text/html"
        self.response.out.write(clientfile.content)

class ClientUpdateHandler(BasePageHandler):
    def get(self):
        self.render("ClientUpdate.html")

    def post(self):
        platform = self.request.get("platform")
        version = int(self.request.get("version"))
        url = self.request.get("url")
        clientversion = ClientVersion(platform = platform, version = version, url = url)
        clientversion.put()
        self.render("ClientUpdate.html")


class PageUpdateHandler(BasePageHandler):
    def get(self):
        self.render("ClientContentUpload.html")

    def post(self):
        values = {}
        pathname = self.request.get("pathname")
        version = int(self.request.get("version"))
        platform = self.request.get("platform")
        content = self.request.get("content")
        clientfile = ClientFile(key_name = client_file_key_name(platform, version, pathname), 
                pathname = pathname,
                version = version,
                platform = platform,
                content = content
                )
        clientfile.put()
        self.render("ClientContentUpload.html", values)

class SignUpHandler(BasePageHandler):
    def get(self):
        self.render("SignUp.html")
    
    def post(self):
        id = self.request.get("id")
        password = self.request.get("password")
        email = self.request.get("email")
        try:
            signup(id, email, password)
            self.redirect('/signup-success') #TODO: signup redirect url here.
        except Exception as e:
            self.render("SignUp.html", {"error": e}) #TODO replace e.strerror with errer messages.


class SignInHandler(BasePageHandler):
    @require_login(None)
    def get(self):
        if self.user: #Already logged in
            self.redirect('/signin-success') #TODO: signin redirect url here.
        self.render("SignIn.html")

    def post(self):
        id = self.request.get("id")
        password = self.request.get("password")
        if signin(id, password):
            set_login(self, id)
            self.redirect('/signin-success') #TODO: signin redirect url here.
        else:
            self.render("SignIn.html", {"error": "Username or Password error"}) #TODO replace e.strerror with errer messages.
        