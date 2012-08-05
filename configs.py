DEBUG = True

router_path = {
            "query_version" : r'/api/client/queryversion', #Query either the client page version or the client version.
            "update_client_page" : r'/page/admin/client_content_upload', # Update a certain client file.
            "admin_channel_list" : r'/page/admin/channels', # List all the channels for edit.
            "admin_channel_update" : r'/page/admin/channel/update', # Update a channel info.
            "admin_video_update" : r'/page/admin/video/update',
            "update_client" : r'/page/admin/client_update', # Update the client.
            "admin_home" : r'/page/admin', # The admin home page. 
        }


