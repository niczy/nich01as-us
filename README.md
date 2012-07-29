##Overview
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
/page/client_content_uploadß

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
None

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







