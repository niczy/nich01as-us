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
		template: '<li><a href="/channel/{{val.channel_id}}/{{val.video_id}}/{{val.id}}"> {{val.comment}}</a><span>Reply</span><div ng-show="false" class="reply-container"><textarea></textarea><button class="btn">Submmit</button></div></li>',
		link: function(scope, element, attrs) {
			if (angular.isArray(scope.val.children)) {
				var replyEle = element.find('span');
				var replyContainer = element.find('div');
				var replyButton = replyContainer.find('button');
				var replyArea = replyContainer.find('textarea');
				replyButton.bind('click', function() {
					replyContainer.hide();
					console.log(replyArea.val());
					var Comment = $resource("/api/addcomment/:channel_id/:video_id/:comment_id", {
						"channel_id": scope.val.channel_id,
						'video_id': scope.val.video_id,
                        'comment_id': scope.val.id,
					});

                    Comment.save({'comment': replyArea.val()}, {}, function(comment){
                        comment.channel_id = scope.val.channel_id;
                        comment.video_id = scope.val.video_id;
                        scope.val.children.push(comment);
                    });
				});

				replyEle.bind('click', function() {
					replyContainer.show();
					console.log(scope.val.comment)
				});
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

function VideoListCntl($scope, $http, $routeParams, $resource) {
	channel = $resource("/api/v/:channel_id")
	offset = $routeParams.offset ? $routeParams.offset: 0;
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

	Like = $resource("/api/video/like");

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

}

function VideoDetailCntl($scope, $routeParams, $resource) {

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
	});

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
			$scope.comments.push(comment);
		});
		$scope.commentContent = '';
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

	$scope.refreshTree = function(comment_id) {
		console.log(comment_id);
	}

	$scope.replyComment = function(commendId) {
		console.log(commentId);
	}
}

