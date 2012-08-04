import webapp2
import handlers
import handlers

class AdminHomeHandler(handlers.BasePageHandler):
    def get(self):
        self.render("AdminHome.html")

