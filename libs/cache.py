'''
Created on Aug 19, 2012

@author: charliezhang
'''

from google.appengine.api import memcache
import hashlib
import configs


def Cached(interval):
    """A decorator that automatically cache the return value of the decorated
    function in memcache, using the serialization of function name and arguments as key.
    
    WARNING: Avoid caching a datastore model object. Some information will loss during
    the serialization/de-serialization. Using the cached datastore object
    may cause extra datastore API calls.
    """
    
    def get_md5(unhased):
        hashed = hashlib.md5()
        hashed.update(unhased)
        return hashed.hexdigest()
    
    def gen_key(fn, *args):
        str_args = map(lambda x: str(x), args)
        str_args.append(fn.__name__)
        return get_md5(','.join(str_args))
        
    def wrapper(fn):
        def inner_wrapper(*args):
            if not configs.CACHE: return fn(*args)
            key = gen_key(fn, *args)
            value = memcache.get(key)
            if not value:
                value = fn(*args)
                memcache.add(key, value, interval)
            return value
        return inner_wrapper
    return wrapper
