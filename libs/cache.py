'''
Created on Aug 19, 2012

@author: charliezhang
'''

from google.appengine.api import memcache
import hashlib

def Cached(interval):
    """A decorator that automatically cache the return value of the decorated
    function in memcache, using the serialization of arguments as key. """
    
    def get_md5(unhased):
        hashed = hashlib.md5()
        hashed.update(unhased)
        return hashed.hexdigest()
    
    def gen_key(*args):
        return get_md5(','.join(map(lambda x: str(x), args)))
        
    def wrapper(fn):
        def inner_wrapper(*args):
            key = gen_key(*args)
            value = memcache.get(key)
            if not value:
                value = fn(*args)
                memcache.add(key, value, interval)
            return value
        return inner_wrapper
    return wrapper
