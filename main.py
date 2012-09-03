#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from handlers import client_page
from handlers import comment_handlers
from handlers import cron_handlers
from handlers import search_handlers
from handlers import video_handlers
from handlers import parser_handlers
from handlers import admin_handlers
from handlers import user_handlers
from handlers import page_handlers
from libs import fastcounter
from configs import router_path
import os

app = webapp2.WSGIApplication([(router_path["query_version"], client_page.VersionQueryHandler),
                                (r'/api/client/getcontent', client_page.PageContentHandler),
                                (r'/api/v/(\w+)', video_handlers.ChannelHandler),
                                (r'/api/v/(\w+)/', video_handlers.ChannelHandler),
                                (r'/api/v/(\w+)/([\w\d\-]+)', video_handlers.VideoHandler),
                                (r'/api/v/(\w+)/(\w+)/', video_handlers.VideoHandler),
                                (r'/api/video/like', video_handlers.VideoLikeHandler),
                                (r'/api/video/dislike', video_handlers.VideoDislikeHandler),
                                (r'/api/getcomment/(\w+)/(\w+)', comment_handlers.CommentHandler),
                                (r'/api/getcomment/(\w+)/(\w+)/([\-\w]+)', comment_handlers.CommentHandler),
                                (r'/api/addcomment', comment_handlers.CommentHandler),
                                (r'/api/addcomment/(\w+)/(\w+)', comment_handlers.CommentHandler),
                                (r'/api/addcomment/(\w+)/(\w+)/(\d+)', comment_handlers.CommentHandler),
                                (r'/api/likecomment/(\w+)/(\w+)/(\d+)', comment_handlers.CommentLikeHandler),
                                (r'/api/dislikecomment/(\w+)/(\w+)/(\d+)', comment_handlers.CommentDislikeHandler),
                                (r'/api/signin', user_handlers.SignInHandler),
                                (r'/api/signout', user_handlers.SignOutHandler),
                                (r'/api/signup', user_handlers.SignUpHandler),
                                (r'/api/userinfo', user_handlers.UserInfoHandler),
                                (r'/task/counter_persist_incr', fastcounter.CounterPersistIncr),
                                (router_path["channel_page"], video_handlers.ChannelPageHandler),
                                (router_path["video_page_with_comment"], video_handlers.VideoPageHandler),
                                (router_path["video_page"], video_handlers.VideoPageHandler),
                                (router_path["update_client_page"], client_page.PageUpdateHandler),
                                (router_path["update_client"], client_page.ClientUpdateHandler),
                                (router_path["admin_channel_update"], admin_handlers.ChannelUpdateHandler),
                                (router_path["admin_channel_list"], video_handlers.ChannelListHandler),
                                (router_path["admin_home"] , admin_handlers.AdminHomeHandler),
                                (router_path["admin_video_update"], admin_handlers.VideoUpdateHandler),
                                (router_path["admin_parser"], admin_handlers.ParserManageHandler),
                                (router_path["admin_start_parse"], admin_handlers.StartParseHandler),
                                (router_path["signup_page"], user_handlers.SignUpPageHandler),
                                (router_path["signin_page"], user_handlers.SignInPageHandler),
                                (router_path["cron_persist_channel"], cron_handlers.PersistChannelListHandler),
                                (router_path["home_page"], page_handlers.HomePageHandler),
                                (router_path["xml_sitemap"], page_handlers.XmlSitemapHandler),
                                (r'/debug', comment_handlers.DebugHandler)
    ],
                              debug=True)
