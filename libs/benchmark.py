'''
Created on Aug 29, 2012

@author: charliezhang
'''
import time
import configs
from libs import fastcounter

def Worktime(name):
    def wrapper(fn):

        def timed(*args, **kw):
            if not configs.BENCHMARK:
                return fn(*args, **kw)
            
            start = time.time()
            result = fn(*args, **kw)
            end = time.time()
            
            fastcounter.incr("Function_%s_NumCalls" % name, 1, 3600)
            fastcounter.incr("Function_%s_TotalMicroSeconds" % name,
                              int((end - start) * 1000000 + 0.5), 3600)
    
            return result
    
        return timed
    return wrapper