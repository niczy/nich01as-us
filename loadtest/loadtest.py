'''
Created on Aug 30, 2012

@author: charliezhang
'''

import time
import os
import re
import httplib
import Queue
import random
from threading import Thread, Lock


# URL parameters
USE_SSL = False  # HTTPS/SSL support
HOST = 'mochadian-loadtest.appspot.com'
MAX_NUM_REQUEST = 1000

# load parameters
THREADS = 5
RAMP_UP = 10 # secs
QPS = 2.0

# response verification
VERIFY_REGEX = '.*'

URLS = [
    "/channel/girls",
    "/channel/girls/15003",
    "/channel/girls/16002",
    "/api/getcomment/girls/17003",
    "/api/getcomment/girls/18002",
    "/api/v/girls",
    "/api/v/girls/20003",
    "/api/v/girls/21003",
    "/signup"
]

def main():
    manager = LoadManager(HOST)
    manager.start(THREADS, THREADS / QPS, VERIFY_REGEX)
    

class LoadManager:
    total_request_cnt = 0
    request_cnt_lock = Lock()
    
    def __init__(self, host):
        self.host = host
        self.start_time = time.time()
        self.q = Queue.Queue()
        LoadManager.request_cnt_lock = Lock()
        LoadManager.total_request_cnt = 0
    
    def start(self, threads=1, interval=0.0, verify_regex='.*'):
        try:
            os.remove('results.csv')
        except:
            pass
        
        # start the thread for reading and writing queued results
        rw = ResultWriter(self.q, self.start_time)
        rw.setDaemon(True)
        rw.start()
        
        # start the agent threads
        agents = []
        for i in range(threads):
            spacing = (float(RAMP_UP) / float(threads))
            if i > 0:
                time.sleep(spacing)
            agent = LoadAgent(self.q, self.host, interval, verify_regex)
            agent.setDaemon(True)
            print 'starting thread # %i' % i
            agent.start()
            agents.append(agent)
        while LoadManager.total_request_cnt < MAX_NUM_REQUEST:
            time.sleep(.25)
        for agent in agents:
            agent.join()

def get_url(host):
    return (host, random.choice(URLS))
    
class LoadAgent(Thread):
    def __init__(self, q, host, interval, verify_regex):
        Thread.__init__(self)
        self.verify_regex = verify_regex
        self.q = q
        self.compiled_verify_regex = re.compile(verify_regex)
        self.host = host
        self.interval = interval
        self.default_timer = time.time
        if USE_SSL:
            self.conn = httplib.HTTPSConnection(host)
        else:
            self.conn = httplib.HTTPConnection(host)
            
    def run(self):
        while True:
            LoadManager.request_cnt_lock.acquire()
            if LoadManager.total_request_cnt >= MAX_NUM_REQUEST:
                LoadManager.request_cnt_lock.release()
                break
            LoadManager.total_request_cnt += 1
            LoadManager.request_cnt_lock.release()
            start = self.default_timer()
            try:
                url = get_url(self.host)
                resp_body, resp_code = self.__send(url)
                finish = self.default_timer()
                self.__verify(resp_body, resp_code, self.compiled_verify_regex)
                verify_passed = 'PASSED'
            except Exception, e:
                print (url[0] + url[1]) + ": " + str(e)
                finish = self.default_timer()
                verify_passed = 'FAILED'
                resp_code = 0
            latency = (finish - start)
            self.q.put((url[0] + url[1], latency, resp_code, verify_passed))
            expire_time = (self.interval - latency)   
            if expire_time > 0:
                time.sleep(expire_time)
                

    def __send(self, url):
        try:
            #conn.set_debuglevel(1)
            self.conn.request('GET', url[1])
            resp = self.conn.getresponse()
            resp_body = resp.read()
            resp_code = resp.status
        except Exception, e:
            raise Exception('Connection Error: %s' % e)
        finally:
            #self.conn.close()
            pass
        return (resp_body, resp_code)
    

    def __verify(self, resp_body, resp_code, compiled_verify_regex):
        if resp_code >= 400:
            raise ValueError('Response Error: HTTP %d Response' % resp_code)
        if not re.search(compiled_verify_regex, resp_body):
            raise Exception('Verification Error: Regex Did Not Match Response')
        return True      



class ResultWriter(Thread):
    def __init__(self, q, start_time):
        Thread.__init__(self)
        self.q = q
        self.start_time = start_time
    

    def run(self):
        f = open('results.csv', 'a')
        while True:
            try:
                q_tuple = self.q.get(False)
                url, latency, resp_code, verify_passed = q_tuple
                f.write('%s %.3f,%i,%s\n' % (url, latency, resp_code, verify_passed))
                f.flush()
                print '%s: %.3f' % (url, latency)
            except Queue.Empty:
                # re-check queue for messages every x sec
                time.sleep(.25)



if __name__ == '__main__':
    main()