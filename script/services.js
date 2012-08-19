angular.module("videoServices", ["ngResource"]).
    factory("videoList", function($resouece){
        return $resource("/api/v/:channel_id"); 
    });
    
