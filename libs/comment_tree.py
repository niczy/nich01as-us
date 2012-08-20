'''
Created on Aug 18, 2012

@author: charliezhang
'''

import datetime
import heapq
import logging
from tools.sort import hot

"""
The tree is represented by its root node
Each 'Node' is a dictionary with the structure: (Some fields are optional)
    "i": int,  // Id of the comment
    "u": str,  // User id
    "c": str,  // Comment text
    "p": int,  // Id of parent comment
    "t": datetime obj,  // Time of creation 
    "s": array of 'Node',  // Sub nodes
    "l": int,  // Like counter
    "d": int,  // Dislike counter
    "n": int,  // total Number of descendants
    "sc": float, // Score
"""

class CommentTree():  
    def __init__(self, comments_model):
        self._root = {'i':-1}
        id_to_comment = {'-1':self._root}
        self._comments = []
        for comment in comments_model:
            comment = comment.to_dict()
            self._comments.append(comment)
            id_to_comment[str(comment["i"])] = comment
        for comment in self._comments:
            pid = str(comment['p'])
            if not id_to_comment.has_key(pid):
                logging.error("Comment data corrupted. Can find parent comment %d for comment %s "
                              % (pid, comment))
                continue
            parent = id_to_comment[pid]
            if not parent.has_key('s'): #sub nodes
                parent['s'] = []
            parent['s'].append(comment)
        _compute_num_descendant_recursive(self._root)
    
    def comments(self):
        return self._comments
        
    def get_sub_tree(self, cid, max_num_comments):
        if cid == -1: root = self._root
        else: root = _find_comment_recursive(self._root, cid)
        return self.get_top_comments(root, max_num_comments)
    
    def get_top_comments(self, root, num_nodes):
        new_root = None
        id_to_nodes = {}
        tree_size = 0
        h = []
        root["sc"] = _score(root)
        heapq.heappush(h, (-root["sc"], root))
        while tree_size < num_nodes and len(h) > 0:
            node = heapq.heappop(h)[1]
            new_node = _copy_node(node)
            if not new_root: new_root = new_node
            if id_to_nodes.has_key(str(node["p"])):
                id_to_nodes[str(node["p"])]["s"].append(new_node)
            id_to_nodes[str(node["i"])] = new_node
            tree_size += 1
            if node.has_key("s"):
                for sub in node["s"]:
                    sub["sc"] = _score(sub)
                    heapq.heappush(h, (-_score(sub), sub))
        return new_root

def _score(node):
    like = dislike = 0
    if node.has_key("l"): like = node["l"]
    if node.has_key("d"): dislike = node["d"]
    return hot(like, dislike, datetime.datetime.strptime(node["t"], "%Y%m%d-%H%S%M"))
    
def _compute_num_descendant_recursive(node):
    num = 0
    if node.has_key('s'):
        for s in node['s']:
            num += _compute_num_descendant_recursive(s)
    node['n'] = num
    return num + 1
    
def _copy_node(node):
    newnode = {}
    for k in node.keys():
        if k != "s":
            newnode[k] = node[k]
    newnode["s"] = []
    return newnode

def _find_comment_recursive(node, id):
    if node['i'] == id: return node
    if not node.has_key('s'): return None
    for sub_node in node['s']:
        ret = _find_comment_recursive(sub_node, id)
        if ret: return ret
    return None   
