'''
Created on Aug 27, 2012

@author: charliezhang
'''


from handlers import BasePageHandler
from models import DataSource as data_source
from datetime import datetime
import configs

class XmlSitemapHandler(BasePageHandler):
    def get(self):
        channel_id = 'girls' #TODO: change channel id
        videos = data_source.get_videos_in_channel(channel_id, 0, 1024)
        values = {}
        values["date"] = datetime.now().strftime("%Y-%m-%d")
        values["host"] = configs.HOST
        values["channel_id"] = channel_id
        values["videos"] = []
        for v in videos:
            values["videos"].append({
                "date": datetime.fromtimestamp(v["modified_datetime"]).strftime("%Y-%m-%d"),
                "id": v["video_id"]
            })
        self.render("Sitemap.xml", values)
    