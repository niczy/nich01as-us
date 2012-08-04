import jinja2
import os
import webapp2
import json
import models

jinja_environment = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
        )

def parse_offset_and_limit(handler, default_offset = 0, max_limit = 64, default_limit = 16):
    offset = default_offset 
    if handler.request.get("offset"):
        offset = int(handler.request.get("offset"))
    limit = default_limit
    if handler.request.get("limit"):
        limit = int(handler.request.get("limit"))
        if limit > max_limit:
            limit = max_limit
    return (offset, limit)


class BasePageHandler(webapp2.RequestHandler):
    def render(self, page_name, values = {}):
        template = jinja_environment.get_template("templates/" + page_name)
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
        


