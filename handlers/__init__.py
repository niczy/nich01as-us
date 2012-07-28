import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
        )


class BasePageHandler(webapp2.RequestHandler):
    def render(self, page_name, values = {}):
        template = jinja_environment.get_template("templates/" + page_name)
        self.response.out.write(template.render(values))


