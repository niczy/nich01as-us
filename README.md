##Overview
For all the api interfaces, the server will return json format data by default.
However, if you specify a "jsonp" parameter in the request, the server will return a jsonp format data.

### Server address

http://video.nich01as.us/

##### API Overview

----
###### Method
Get

###### Path
/api/client/getcontent

###### Parameters
platform: A string indicate which platform you are requesting.

pathname: A string indicate the relative file path. 

version: A integer indicate the version number specified file.

###### Return
This interface will return the content of the file.

----
###### Method
Get

###### Path
/api/client/queryversion

###### Parameters
platform: A string indicate which platform you are requesting.

pathname: A string indicate the relative file path. If this parameter is missing, the server will return the client update info.

###### Return
Return a integer, which represents the latest version of that file.
Or return the latest version number of the client as well as the download url.

----

###### Method
Get

###### Path
/page/client_content_upload

###### Parameters
None

###### Return
This is a manage page for update certain file.

----
###### Method
Get

###### Path
/page/client_update

###### Parameters
None

###### Return
This is a manage page for update client version.

----

###### Method
Get

###### Path
/api/v/{channel_id}


###### Parameters
offset: Speficy the offset for the video list. Default value 0.

limit: Specify how many videos returned at most. Default value 16. Maxvalue 64.

###### Return
Return the channel infomation, inclues its  videos.

----

###### Method
Get

###### Path
/api/v/{channel_id}/{video_id}

###### Parameters
None

###### Return
Return the video information.

----

to like a video.
###### method
post


###### path
/api/video/like
###### parameters

channel_id: the channel_id.

video_id: the video_id.

###### return
return the video information.

----


to dislike a video.
###### method
post


###### path
/api/video/dislike
###### parameters

channel_id: the channel_id.

video_id: the video_id.

###### return
return the video information.

----





to like a video.
to like a video.








