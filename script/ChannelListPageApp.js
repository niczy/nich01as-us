angular.module('CommentsTree', []);

angular.module('App', ['ngResource', 'CommentsTree']).
config(function($routeProvider, $locationProvider) {
	$routeProvider.
	when('/channel/:channel_id', {
		templateUrl: "/partials/VideoList.html",
		controller: VideoListCntl
	}).
	when('/channel/:channel_id/:video_id', {
		templateUrl: "/partials/VideoDetail.html",
		controller: VideoDetailCntl
	}).
	when('/channel/:channel_id/:video_id/:comment_id', {
		templateUrl: "/partials/VideoDetail.html",
		controller: VideoDetailCntl
	});;
	$locationProvider.html5Mode(true);
});

angular.module('CommentsTree').filter('ifarray', function() {
	return function(input) {
		return $.isArray(input) ? input: [];
	}
}).directive('treenode', function($compile, $resource) {
	return {
		restrict: 'A',
		terminal: true,
		scope: {
			val: '=val'
		},
		template: '<li class="tree-node"><a class="comment_content" href="/channel/{{val.channel_id}}/{{val.video_id}}/{{val.id}}"> {{val.comment}}</a><span class="comment-user"><font>({{val.user}})</font></span><a class="btn-link">回复</a><div ng-show="false" class="reply-container"><textarea class=""></textarea><div><span ng-show="false" class="alert alert-error">请先登陆</span><button class="btn btn-primary">确定</button></div></div></li>',
		link: function(scope, element, attrs) {
			if (angular.isArray(scope.val.children)) {
				var replyEle = angular.element(element.find('a')[1]);
				var replyContainer = element.find('div');
				var replyButton = replyContainer.find('button');
				var replyArea = replyContainer.find('textarea');
                var replyError = replyContainer.find("span");
                var opend = false;
                var Comment = $resource("/api/addcomment/:channel_id/:video_id/:comment_id", {
						"channel_id": scope.val.channel_id,
						'video_id': scope.val.video_id,
                        'comment_id': scope.val.id,
					});

				replyButton.bind('click', function() {
					console.log(replyArea.val());
					
                    Comment.save({'comment': replyArea.val()}, {}, function(comment){
                        if (comment["error_code"] === 1) {
                            replyError.show();
                            return;
                        }
                        comment.channel_id = scope.val.channel_id;
                        comment.video_id = scope.val.video_id;
                        var tmpComment = [comment];
                        scope.val.children = tmpComment.concat(scope.val.children);
                        replyArea.val("");
                        toogleReply();
                        replyError.hide();
                    });
				});

				replyEle.bind('click', function() {
                    if (opend) {
                        replyContainer.hide();
                        opend = false;
                        replyEle.html("回复");
                    } else {
                        replyContainer.show();
                        opend = true;
                        replyEle.html("取消");
                    }
					console.log(scope.val.comment)
				});

                function toogleReply() {
                    if (opend) {
                        replyContainer.hide();
                        opend = false;
                        replyEle.html("回复");
                    } else {
                        replyContainer.show();
                        opend = true;
                        replyEle.html("取消");
                    }
                }
			}
			element.append('<div tree val="val.children"></div>');
			$compile(element.contents())(scope.$new());

		}
	}
}).directive('tree', function($compile) {
	return {
		restrict: 'A',
		terminal: true,
		scope: {
			val: '=val',
		},

		link: function(scope, element, attrs) {
			if (angular.isArray(scope.val)) {
				element.append('<ul><div ng-repeat="item in val"><div treenode val="item"></div></div></ul>');
			}
			$compile(element.contents())(scope.$new());
		}
	}
});

function VideoListCntl($scope, $http, $routeParams, $resource, $window) {

    $window.document.title = "抹茶店 娱乐资讯";
	channel = $resource("/api/v/:channel_id")
	offset = $routeParams.offset ? $routeParams.offset: 0;

    $scope.offset = offset;
	channel.get({
		'channel_id': 'girls',
		'offset': offset
	},
	function(data) {
		$scope.videos = data.videos;
		$scope.channel = data.channel;
		$scope.offset = data.offset;
		$scope.limit = data.limit;
	})


	function findVideo(videos, video) {
		for (var i = 0; i < videos.length; i++) {
			if (videos[i].channel_id == video.channel_id && videos[i].video_id == video.video_id) {
				return i;
			}
		}
		return - 1;
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


	Like = $resource("/api/video/like");

	$scope.like = function(channel_id, video_id) {
		Like.get({
			"channel_id": channel_id,
			"video_id": video_id
		},
		function(video) {
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
		Dislike.get({
			"channel_id": channel_id,
			"video_id": video_id
		},
		function(video) {
			var i = findVideo($scope.videos, video);
			if (i >= 0) {
				$scope.videos[i] = video;
				sortVideos();
			}
		});
	}

    $scope.userName = 'fuck';

}

function VideoDetailCntl($scope, $routeParams, $resource, $window) {

	var commentId = - 1;
	if ($routeParams.comment_id != undefined) {
		commentId = $routeParams.comment_id;
	}

	$scope.comment_id = commentId;

	var Video = $resource("/api/v/:channel_id/:video_id");
	$scope.video = Video.get({
		'channel_id': $routeParams.channel_id,
		'video_id': $routeParams.video_id
	},
	function(video) {
		console.log(video);
		var youkuPlayer = '<embed id="STK_134545267189696" height="356" allowscriptaccess="never" style="visibility: visible;" pluginspage="http://get.adobe.com/cn/flashplayer/" flashvars="playMovie=true&amp;auto=1" width="440" allowfullscreen="true" quality="hight" src="http://player.youku.com/player.php/sid/YOUKUID=/v.swf" type="application/x-shockwave-flash" wmode="transparent">'.replace('YOUKUID', video.external_id);
		$('#video-container').html(youkuPlayer);
        $window.document.title = video.title;  
	}
    );

	var Comment = $resource("/api/addcomment/:channel_id/:video_id/:comment_id", {
		"channel_id": $routeParams.channel_id,
		'video_id': $routeParams.video_id
	});

	$scope.comments = [];

	$scope.addComment = function() {
		Comment.save({
			'comment': $scope.commentContent
		},
		{},
		function(comment) {
			console.log(comment);
			console.log('comment succeed');
            if (comment['error_code'] === 1) {
                $scope.commentError = "请先登陆";
                return;
            }
            comment.channel_id = $routeParams.channel_id;
            comment.video_id = $routeParams.video_id;
            var tmpComments = [comment];
            $scope.comments = tmpComments.concat($scope.comments);
            $scope.commentContent = '';
            $scope.commentError = "";
		});
	}

	var Comments = $resource('/api/getcomment/:channel_id/:video_id/:comment_id', {
		'channel_id': $routeParams.channel_id,
		'video_id': $routeParams.video_id,
		'comment_id': commentId
	});
	$scope.comments = Comments.query(function(comments) {
		extendInfo($scope.comments);
	});

	function extendInfo(comments) {
		angular.forEach(comments, function(v, k) {
			v.channel_id = $routeParams.channel_id;
			v.video_id = $routeParams.video_id;
			extendInfo(v.children);
		});
	}

	$scope.refreshTree = function() {
        $scope.comments = Comments.query(function(comments) {
            extendInfo($scope.comments);
        });
	}

	$scope.replyComment = function(commendId) {
		console.log(commentId);
	}

    Like = $resource("/api/video/like");

	$scope.like = function(channel_id, video_id) {
		$scope.video = Like.get({
			"channel_id": channel_id,
			"video_id": video_id
		});
	}

	Dislike = $resource("/api/video/dislike");

	$scope.dislike = function(channel_id, video_id) {
		$scope.video = Dislike.get({
			"channel_id": channel_id,
			"video_id": video_id
		});
	}

}


function UserCntl($scope, $resource) {

    var Userinfo = $resource("/api/userinfo");

    Userinfo.get(function(data) {
        if (data["id"] != undefined) {
            $scope.loginUser = data["id"];
        }
    });
    var Signin = $resource("/api/signin");
    $scope.login = function login() {
        console.log("login clicked" + $scope.userName);
        Signin.get({"id": $scope.userName, "password": $scope.password}, function(data) {
            console.log(data);
            if (data["id"] == undefined) {
                $scope.loginError = data["error"];
            } else {
                $scope.loginUser = data["id"];
                $scope.loginError = "";
                $scope.hideLogin();
            }
        });
    }

    var Signup = $resource("/api/signup");

    $scope.regist = function() {
        console.log("regist clicked" + $scope.rUserName);

        if ($scope.rPassword != $scope.rVerifyPassword) {
            $scope.registError = "两次输入的密码不一致，请重新输入";
            return;
        }
        var args = {"id": $scope.rUserName, "password": $scope.rPassword};
        if ($scope.rEmail != undefined) {
            args["rEmail"] = $scope.rEmail;
        }
        Signup.get(args, function(data) {
            console.log(data);
            if (data["id"] != undefined) {
                $scope.loginUser = data["id"];
                $scope.registError = "";
                $scope.hideLogin();
            } else {
                $scope.registError = data["error"];
            }
        });
    }

    $scope.showOverflow = false;

    $scope.showLogin = function() {
        $scope.showOverflow = true;
    }

    $scope.hideLogin = function() {
        $scope.showOverflow = false;
    }

    var Logout = $resource("/api/signout");

    $scope.logout = function() {
        Logout.get(function(data) {
           $scope.loginUser = ""; 
        });
    }


}
