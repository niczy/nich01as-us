angular.module('App', ['ngResource']).
    config(function($routeProvider, $locationProvider) {
        $routeProvider.
            when('/channel/:channel_id', {templateUrl:"/partials/VideoList.html", controller:VideoListCntl}).
            when('/channel/:channel_id/:video_id', {templateUrl:"/partials/VideoDetail.html", controller: VideoDetailCntl});
        $locationProvider.html5Mode(true);
    });

function VideoListCntl($scope, $http, $routeParams, $resource) {
    channel = $resource("/api/v/:channel_id")
    offset = $routeParams.offset ? $routeParams.offset : 0;
    channel.get({'channel_id': 'girls', 'offset': offset}, function(data){
        $scope.videos = data.videos;
        $scope.channel = data.channel;
        $scope.offset = data.offset;
        $scope.limit = data.limit;
    })

    Like = $resource("/api/video/like");

    function findVideo(videos, video) {
        for (var i = 0; i < videos.length; i++) {
            if (videos[i].channel_id == video.channel_id && videos[i].video_id == video.video_id) {
                return i;
            }
        }
        return -1;
    }

    function sortVideos() {
        for (var i = 0; i < $scope.videos.length; i++) {
            for (var j = i + 1; j < $scope.videos.length; j++) {
                if ($scope.videos[j].final_score > $scope.videos[i].final_score) {
                    console.log("swaped");
                    var tmp = $scope.videos[i];
                    $scope.videos[i] = $scope.videos[j];
                    $scope.videos[j] = tmp;
                } else {
                    console.log($scope.videos[j].final_score + " " + $scope.videos[i].final_score + " no swap");

                }
            }
        }
    }

    $scope.like = function(channel_id, video_id) {
        Like.get({"channel_id": channel_id, "video_id": video_id}, function(video){
            var i = findVideo($scope.videos, video);
            if (i >= 0) {
                $scope.videos[i] = video;
                sortVideos();
            }
            console.log(video) 
        });
    }

    Dislike = $resource("/api/video/dislike");

    $scope.dislike = function(channel_id, video_id) {
        Dislike.get({"channel_id": channel_id, "video_id": video_id}, function(video){
            var i = findVideo($scope.videos, video);
            if (i >= 0) {
                $scope.videos[i] = video;
                sortVideos();
            }
        });
    }
    
}


function VideoDetailCntl($scope, $routeParams, $resource, $window) {
    console.log("In Video Detail Cntl");
    var Video = $resource("/api/v/:channel_id/:video_id");
    $scope.video = Video.get({'channel_id': $routeParams.channel_id, 'video_id': $routeParams.video_id}, function (video) {
        console.log(video);
    var youkuPlayer = '<embed id="STK_134545267189696" height="356" allowscriptaccess="never" style="visibility: visible;" pluginspage="http://get.adobe.com/cn/flashplayer/" flashvars="playMovie=true&amp;auto=1" width="440" allowfullscreen="true" quality="hight" src="http://player.youku.com/player.php/sid/YOUKUID=/v.swf" type="application/x-shockwave-flash" wmode="transparent">'.replace('YOUKUID', video.external_id);
    $('#video-container').html(youkuPlayer);
    });


    $scope.comments = ['a', 'b'];

    $scope.addComment = function() {
        $scope.comments.push($scope.commentContent);
        $scope.commentContent = '';
    }
}



