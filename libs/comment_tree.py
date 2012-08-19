'''
Created on Aug 18, 2012

@author: charliezhang
'''

import logging

class CommentTree():  
    def __init__(self, comments_model):
        self._root = {'i':-1}
        id_to_comment = {'-1':self._root}
        comments = []
        for comment in comments_model:
            comment = comment.to_dict()
            comments.append(comment)
            id_to_comment.update({str(comment["i"]):comment})
        for comment in comments:
            pid = str(comment['p'])
            if not id_to_comment.has_key(pid):
                logging.error("Comment data corrupted. Can find parent comment %d for comment %s "
                              % (pid, comment))
                continue
            parent = id_to_comment[pid]
            if not parent.has_key('s'): #sub nodes
                parent.update({'s': []})
            parent['s'].append(comment)
    
    @staticmethod
    def find_comment_recursive(node, id):
        if node['i'] == id: return node
        if not node.has_key('s'): return None
        for sub_node in node['s']:
            ret = CommentTree.find_comment_recursive(sub_node, id)
            if ret: return ret
        return None
    
    def get_sub_tree(self, cid):        
        if cid == -1: return self._root
        return CommentTree.find_comment_recursive(self._root, cid)