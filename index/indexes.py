'''
Created on Jul 29, 2012

@author: charliezhang
'''

import json
import logging
from google.appengine.api import search
from models.VideoModels import ChannelModel
from models.VideoModels import VideoModel

def get_field_value(fields, name):
    for f in fields:
        if f.name == name:
            return f.value
    return None
    
class AbstractIndex():
    '''
    Base class for all indexes.
    '''
    
    name = None
    
    def model_do_document(self, model):
        pass

    def returned_fields(self):
        pass
    
    def snippeted_fields(self):
        pass
    
    '''
    Items above should be customized for each index.
    '''
    
    def add(self, model):
        document = self.model_do_document(model)
        try:
            self.get_index().add(document)
        except search.Error as e:
            logging.exception("Failed to add doc %s to index %s, error: %s."
                              % (document.doc_id, self.name. e.strerror))
    
    def search(self, raw_query):
        options = search.QueryOptions(
            limit=10,  # the number of results to return
            cursor=None,
            returned_fields=self.returned_fields(),
            snippeted_fields=self.snippeted_fields())
        query = search.Query(query_string=raw_query, options=options)
        results = []
        try:
            results = self.get_index().search(query).results
        except search.Error:
            logging.exception('Search to index %s failed, raw_query: %s, query: %s'
                              % (self.name, raw_query, query))
            return []
        results_dict = []
        for r in results:
            val = get_field_value(r.fields, 'payload')
            results_dict.append(json.loads(val))
        return results_dict

    def get_index(self):
        return search.Index(name=self.name, consistency=search.Index.PER_DOCUMENT_CONSISTENT)
    
class VideoIndex(AbstractIndex):
    '''
    Index for videos.
    '''

    name = 'IDX_VIDEOS'
    
    def model_do_document(self, video):
        return search.Document(
            doc_id=str(video.key().id()),
            fields=[search.TextField(name='title', value=video.title),
                    search.TextField(name='payload', value=json.dumps(video.to_dict())),
                      ],
            language='zh')
        
    def returned_fields(self):
        return ['title', 'payload']
    
    def snippeted_fields(self):
        return ['title']
    
class ChannelIndex(AbstractIndex):
    '''
    Index for channels.
    '''

    name = 'IDX_CHANNELS'
    
    def model_do_document(self, channel):
        return search.Document(
            doc_id=channel.key().name(),
            fields=[search.TextField(name='title', value=channel.title),
                    search.TextField(name='payload', value=json.dumps(channel.to_dict())),
                      ],
            language='zh')    
          
    def returned_fields(self):
        return ['title', 'payload']
    
    def snippeted_fields(self):
        return ['title']
        