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
from handlers import video_handlers
from handlers import parser_handlers
from handlers import admin_handlers
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
                                (router_path["update_client_page"], client_page.PageUpdateHandler),
                                (router_path["update_client"], client_page.ClientUpdateHandler),
                                (router_path["admin_channel_update"], admin_handlers.ChannelUpdateHandler),
                                (router_path["admin_channel_list"], video_handlers.ChannelListHandler),
                                (router_path["admin_home"] , admin_handlers.AdminHomeHandler),
                                (router_path["admin_video_update"], admin_handlers.VideoUpdateHandler),
                                (router_path["admin_parser"], admin_handlers.ParserManageHandler),
    ],
                              debug=True)
