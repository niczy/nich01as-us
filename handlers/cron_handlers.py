'''
Created on Aug 27, 2012

@author: charliezhang
'''

import handlers
import logging
from google.appengine.api import taskqueue
from models import DataSource as data_source
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel
from configs import router_path

MAX_NUM_CHANNELS = 1000

class PersistChannelListHandler(handlers.BasePageHandler):
    def get(self):
        channels = ChannelModel.all().fetch(MAX_NUM_CHANNELS)
        for c in channels:
          taskqueue.add(url = router_path["cron_persist_channel"],
                        params = {"name": "persist_channel", "channel_id": c.key().name()})
        #self.render("ParserManage.html")
    
    def post(self):
        channel_id = self.request.get("channel_id")
        logging.info("Persisting data in channel: %s" % channel_id)
        videos = data_source.get_videos_in_channel(channel_id, 0, data_source.MAX_CHANNEL_SIZE)
        logging.info("Got videos: %d" % len(videos))
        for v in videos:   
            video_model = data_source.get_video_model(channel_id, v["video_id"])
            video_model.final_score = v["final_score"]
            logging.info("Updating video %d with final_score %f" % (v["video_id"], v["final_score"]))
            video_model.put()
        #self.render("ParserManage.html")