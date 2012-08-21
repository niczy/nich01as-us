'''
Created on Aug 18, 2012

@author: charliezhang
'''

import handlers
from handlers import require_login
from models.DataSource import get_comment_tree
from models.DataSource import add_comment
from models.DataSource import like_comment
from models.DataSource import dislike_comment
import logging
from libs import comment_tree

class CommentHandler(handlers.BaseJsonHandler):
    '''
    Return the comment tree rooted from a comment.
    '''
    def get(self, channel_id, video_id, comment_id='-1'):
        num = self.request.get("num")
        if num: tree = get_comment_tree(channel_id, video_id, int(comment_id), int(num))  
        else: tree = get_comment_tree(channel_id, video_id, int(comment_id)) 
        comments = comment_tree.readable_comment_list(tree)        
        if tree:
            self.render_dict_as_json(comments)
        else:
            self.response.out.write("comment tree not found")
    
    '''
    Add a comment under the given comment id.
    '''
    @require_login('/')
    def post(self, channel_id = None, video_id = None, comment_id='-1'):
        comment_content = self.request.get('comment')
        logging.info(self.request.body)
        comment = add_comment(comment_content, self.user, channel_id, video_id, comment_id)
        self.render_dict_as_json(comment.to_dict())

class CommentLikeHandler(handlers.BaseJsonHandler):
    '''
    To like a comment
    '''
    def post(self, channel_id, video_id, comment_id):
        delta = int(self.request.get('delta'))
        like_comment(channel_id, video_id, comment_id, delta)

    def get(self):
        pass

class CommentDislikeHandler(handlers.BaseJsonHandler):
    '''
    To dislike a comment
    '''
    def post(self, channel_id, video_id, comment_id):
        delta = int(self.request.get('delta'))
        dislike_comment(channel_id, video_id, comment_id, delta)

    def get(self):
        pass

class DebugHandler(handlers.BasePageHandler):
    
    def get(self):
        self.render("Debug.html", {})
