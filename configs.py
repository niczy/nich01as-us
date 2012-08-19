DEBUG = True

router_path = {
            "query_version" : r'/api/client/queryversion', #Query either the client page version or the client version.
            "update_client_page" : r'/page/admin/client_content_upload', # Update a certain client file.
            "update_client" : r'/page/admin/client_update', # Update the client.
            "admin_channel_list" : r'/page/admin/channels', # List all the channels for edit.
            "admin_channel_update" : r'/page/admin/channel/update', # Update a channel info.
            "admin_video_update" : r'/page/admin/video/update',
            'admin_parser' : r'/page/admin/parser', # Page used to manage the parsers
            "admin_home" : r'/page/admin', # The admin home page. 
            "admin_start_parse" : r'/page/admin/parse/start',
            "channel_page": r'/channel/(\w+)', 
            "signup_page": r'/signup',
            "signin_page": r'/signin',
        }


