import jinja2
import os
import webapp2
import json
import models

jinja_environment = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
        )


class BasePageHandler(webapp2.RequestHandler):
    def render(self, page_name, values = {}):
        template = jinja_environment.get_template("templates/" + page_name)
        self.response.out.write(template.render(values))

class BaseJsonHandler(webapp2.RequestHandler):
    def render_dict_as_json(self, json_dict):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_dict))

    def redner_model_as_json(self, json_model):
        self.render_dict_as_json(json_model.to_dict())
        


