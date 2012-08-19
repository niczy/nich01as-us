function VideoListCntl($scope, $http, $routeParams, $resource, videoList) {
    videoList.get({'channel_id': 'girls'}, function(data){
        console.log(data); 
    })
    $http.get("/api/v/girls").success(function(data){
        console.log(data);
        $scope.videos = data.videos
    });        
    console.log($routeParams)
}



