'''
Created on Jul 29, 2012

@author: charliezhang
'''

import handlers
from index.indexes import ChannelIndex
from index.indexes import VideoIndex

class ChannelSearchHandler(handlers.BaseJsonHandler):
    def get(self, query):
        self.render_dict_as_json(ChannelIndex().search(query))
        
class VideoSearchHandler(handlers.BaseJsonHandler):
    def get(self, query):
        self.render_dict_as_json(VideoIndex().search(query))