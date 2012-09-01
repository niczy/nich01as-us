'''
Created on Aug 30, 2012

@author: charliezhang
'''


"""Fast counter library for App Engine.

Counter increments generally only touch memcache, and occasionally enqueue a
task.  Both are very fast and low overhead.  The downside is that the counter
could undercount (e.g., if memcache data is evicted before it is persisted via
a task).  The task which increments the datastore-based counter is not
idempotent and would double-count if ran extra time(s).  However, this should
be rather exceptional based on App Engine's documentation.
"""
import logging
import random
import webapp2
from google.appengine.api import memcache
from google.appengine.api.taskqueue import taskqueue
from google.appengine.ext import db
from configs import DEBUG

__all__ = ['get_count', 'get_counts', 'incr']

UPDATE_INTERVAL = 3600

class Counter(db.Model):
    """Persistent storage of a counter's values"""
    # key_name is the counter's name
    value = db.IntegerProperty(indexed=False, default=0)


def get_count(name):
    """Returns the count of the specified counter name.

    If it doesn't exist, 0 is returned.
    """

    mc = memcache.get("ctr_val:" + name);
    if mc is None:
        counter = Counter.get_by_key_name(name)
        if counter is None: mc = 0
        else: mc = counter.value
        memcache.add("ctr_val:" + name, mc, 86400)
    return mc

def get_counts(names):
    """Like get_count, but fetches multiple counts at once which is much
    more efficient than getting them one at a time.
    """
    mc_counts = memcache.get_multi(names, 'ctr_val:')
    ret = []
    for i, name in enumerate(names):
        if not mc_counts.has_key(name):
            mc_counts[name] = get_count(name)
        mc_count = mc_counts[name]
        ret.append(mc_count)
    return ret

def incr(name, delta=1):
    """Increments a counter.  The increment is generally a memcache-only
    operation, though a task will also be enqueued about once per
    update_interval.  May under-count if memcache contents is lost.

    Args:
      name: The name of the counter.
      delta: Amount to increment counter by, defaulting to 1.
      update_interval: Approximate interval, in seconds, between updates.  Must
                       be greater than zero.
    """
    lock_key = "ctr_lck:" + name
    delta_key = "ctr_val:" + name
    
    # update memcache
    if delta >= 0:
        v = memcache.incr(delta_key, delta, initial_value = 0)
    elif delta < 0:
        v = memcache.decr(delta_key, -delta, initial_value = 0)
        
    if memcache.add(lock_key, None, time=UPDATE_INTERVAL):
        # time to enqueue a new task to persist the counter
        # note: cast to int on next line is due to GAE issue 2012
        # (http://code.google.com/p/googleappengine/issues/detail?id=2012)
        v = int(v)
        try:
            qn = random.randint(0, 4)
            qname = 'PersistCounter%d' % qn
            taskqueue.add(url='/task/counter_persist_incr',
                          queue_name=qname,
                          params=dict(name=name,
                                      value=v))
        except:
            # task queue failed but we already put the delta in memcache;
            # just try to enqueue the task again next interval
            return

class CounterPersistIncr(webapp2.RequestHandler):
    """Task handler for incrementing the datastore's counter value."""
    def post(self):
        name = self.request.get('name')
        value = int(self.request.get('value'))
        db.run_in_transaction(CounterPersistIncr.incr_counter, name, value)

    @staticmethod
    def incr_counter(name, value):
        c = Counter.get_by_key_name(name)
        if c is None:
            c = Counter(key_name=name, value=value)
        else:
            c.value = value
        c.put()