'''
Created on Aug 18, 2012

@author: charliezhang
'''

from google.appengine.ext import db
import hashlib

PASSWORD_HASH_KEY = "THISISARANDOMSEQUENCE4108s981sdnvSKJFN192!AAS"
USER_COOKIE_HASH_KEY = "THISISANOTHERRANDOMSEQUENCE23498q823jhfZKJFDQS%^%$"

def get_user_cookie_key(id):
    hashed = hashlib.md5()
    hashed.update(USER_COOKIE_HASH_KEY + str(id))
    return hashed.hexdigest()

def get_hashed_password(pw):
    hashed = hashlib.md5()
    hashed.update(PASSWORD_HASH_KEY + str(pw))
    return hashed.hexdigest()

    
def set_login(handler, id):
    cookie_key = get_user_cookie_key(id)
    handler.response.headers.add_header('Set-Cookie','id=' + str(id) + '; expires=Sun, 31-May-2999 23:59:59 GMT; path=/;')
    handler.response.headers.add_header('Set-Cookie','key=' + cookie_key + '; expires=Sun, 31-May-2999 23:59:59 GMT; path=/;')

def logout(hanlder):
    handler.response.headers.add_header('Set-Cookie','id=deleted; expires=Sun, 31-May-1971 23:59:59 GMT; path=/;')
    handler.response.headers.add_header('Set-Cookie','key=deleted; expires=Sun, 31-May-1971 23:59:59 GMT; path=/;')
    
# Try signup, return true if succeeded, raise error if user existed.
def signup(id, email, password):   
    users = db.Query(User).filter("id =", id).fetch(limit = 1)
    for u in users:
        raise Exception("id %s already exist." % id)
    users = db.Query(User).filter("email =", email).fetch(limit = 1)
    for u in users:
        raise Exception("email address %s is already taken." % email)
    user = User(id = id, password = get_hashed_password(password), email = email)
    user.put()
    return True

# Signin with id or email, return true if succeeded, false otherwise.
def signin(id, password):  
    users = db.Query(User).filter("id =", id).fetch(limit = 1)
    hashed_pw = get_hashed_password(password)
    for u in users:
        if hashed_pw == u.password:
            return True
    return False

class User(db.Model):
    id = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False, indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
