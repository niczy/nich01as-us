'''
Created on Aug 25, 2012

@author: charliezhang
'''
import handlers
from handlers import BasePageHandler
from handlers import BaseJsonHandler
from handlers import ErrorCodes
from handlers import require_login
from handlers import require_login_json

from models.UserModels import signup
from models.UserModels import signin
from models.UserModels import logout
from models.UserModels import set_login

import configs

class UserInfoHandler(BaseJsonHandler):

    def get(self):
        handlers._get_user_id(self);
        if self.user:
            self.render_dict_as_json({"id": self.user});
        else:
            self.render_dict_as_json({});

class SignUpHandler(BaseJsonHandler):
    def post(self):
        id = self.request.get("id")
        password = self.request.get("password")
        email = self.request.get("email")
        try:
            signup(id, email, password)
            set_login(self, id)
            self.render_dict_as_json({'id': id})
        except Exception as e:
            msg = 'sign up failed. '
            if configs.DEBUG: msg += str(e)
            self.error(ErrorCodes.SIGNUP_FAILED, msg)
    
    def get(self):
        if configs.DEBUG:
            return self.post()

class SignInHandler(BaseJsonHandler):
    def post(self):
        id = self.request.get("id")
        password = self.request.get("password")
        try:
            signin(id, password)
            set_login(self, id)
            self.render_dict_as_json({'id': id})
        except Exception as e:
            msg = 'sign in failed. '
            if configs.DEBUG: msg += str(e)
            self.error(ErrorCodes.SIGNIN_FAILED, msg)
    
    def get(self):
        if configs.DEBUG:
            return self.post()

class SignOutHandler(BaseJsonHandler):
    @require_login_json(ErrorCodes.NOT_LOGGED_IN, 'Not logged in')
    def post(self):
        logout(self)
        self.render_dict_as_json({'id': self.user})
    
    def get(self):
        if configs.DEBUG:
            return self.post()
                        
class SignUpPageHandler(BasePageHandler):
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


class SignInPageHandler(BasePageHandler):
    @require_login(None)
    def get(self):
        if self.user: #Already logged in
            self.redirect('/signin-success') #TODO: signin redirect url here.
        self.render("SignIn.html")

    def post(self):
        id = self.request.get("id")
        password = self.request.get("password")
        try:
            signin(id, password)
            set_login(self, id)
            self.redirect('/signin-success') #TODO: signin redirect url here.
        except Exception as e:
            self.render("SignIn.html", {"error": "Username or Password error"}) #TODO replace e.strerror with errer messages.
