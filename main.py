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
import os

app = webapp2.WSGIApplication([(r'/api/client/queryversion', client_page.VersionQueryHandler),
                                (r'/api/client/getcontent', client_page.PageContentHandler),
                                (r'/api/v/(\w+)', video_handlers.ChannelHandler),
                                (r'/api/v/(\w+)/', video_handlers.ChannelHandler),
                                (r'/api/v/(\w+)/([\w\d\-]+)', video_handlers.VideoHandler),
                                (r'/api/v/(\w+)/(\w+)/', video_handlers.VideoHandler),
                                (r'/api/video/like', video_handlers.VideoLikeHandler),
                                (r'/api/video/dislike', video_handlers.VideoDislikeHandler),
                                (r'/page/client_content_upload', client_page.PageUpdateHandler),
                                (r'/page/client_update', client_page.ClientUpdateHandler),
                                (r'/page/channel_manage', video_handlers.ChannelManageHandler),
                                (r'/page/video_manage', video_handlers.VideoManageHandler),
                                (r'/page/manage/parser', parser_handlers.YoukuParserHandler),
    ],
                              debug=True)
