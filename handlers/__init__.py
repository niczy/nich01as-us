import jinja2
import os
import webapp2
import json
import models
from configs import router_path
from models import UserModels

jinja_environment = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
        )

def parse_offset_and_limit(handler, default_offset = 0, max_limit = 64, default_limit = 16):
    offset = default_offset 
    if handler.request.get("offset"):
        offset = int(handler.request.get("offset"))
        if offset < 0:
            offset = 0
    limit = default_limit
    if handler.request.get("limit"):
        limit = int(handler.request.get("limit"))
        if limit > max_limit:
            limit = max_limit
    return (offset, limit)

# Decorator applies to get/post methods that requires user's information.
# If the user already logged in, self.user will contain the user's id or email,
# otherwise None.
# If the 'url' argument is provided, unlogged-in users will be
# redirected to 'url'
def require_login(url = None):
    def login_check(fn):
        def Get(self, *args):
            self.user = self.request.cookies.get('id')
            if self.user:
                key = self.request.cookies.get('key')
                expected_key = UserModels.get_user_cookie_key(self.user)
                if key != expected_key:
                    self.user = None
                    
            if self.user == None and url != None:
                self.redirect(url)
                return
            else:
                fn(self, *args)
        return Get
    return login_check

class BasePageHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        webapp2.RequestHandler.__init__(self, request, response)
        self.user = None
        
    def render(self, page_name, values = {}):
        template = jinja_environment.get_template("templates/" + page_name)
        values["routers"] = router_path
        if self.user:
            values["user"] = self.user
        self.response.out.write(template.render(values))

class BaseJsonHandler(webapp2.RequestHandler):
    def render_dict_as_json(self, json_dict):
        if self.request.get("jsonp"):
            self.response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
            self.response.out.write('%s(%s)' % (self.request.get("jsonp"), json.dumps(json_dict)))
        else:
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            self.response.out.write(json.dumps(json_dict))

    def redner_model_as_json(self, json_model):
        self.render_dict_as_json(json_model.to_dict())
