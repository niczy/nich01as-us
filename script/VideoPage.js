angular.module('App', ['ngResource']).
    config(function($routeProvider, $locationProvider) {
        $routeProvider.
            when('/channel/:channel_id/:video_id', {templateUrl:"/partials/VideoComments.html", controller:VideoCommentsCntl});
        $locationProvider.html5Mode(true);
    });

function VideoCommentsCntl($resource) {

}


