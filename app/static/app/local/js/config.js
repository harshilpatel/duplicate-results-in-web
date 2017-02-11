var app = angular.module('app', ['ngRoute', 'ngAnimate', 'ngResource'])

app.factory('QUERY', function($resource){
    return $resource('/tool/search');
})

app.controller('search', function($scope, QUERY){
    $scope.query = "";
    $scope.queryQuantity = 100;
    $scope.queryForce = false;

    $scope.search = function(){
        $("#submitQuery").removeClass('btn-danger');
        if($scope.query.length > 0){
            $("#submitQuery").attr('disabled', 'disabled');
            $scope.results = QUERY.query({query:$scope.query,
                                        quantity:$scope.queryQuantity,
                                        force:$scope.queryForce,
                                            }, function(){
                                                $("#submitQuery").removeAttr('disabled');
                                            });
        } else{
            $("#submitQuery").addClass('btn-danger');
        }
    }
})

app.controller('compare', function($scope){

})


app.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/tool/home', {
        templateUrl: 'search.htm',
        controller: 'search',
      })
      .when('/tool/compare', {
        templateUrl: 'compare.htm',
        controller: 'compare',
      })
      .otherwise('/tool/home')

    // $locationProvider.html5Mode(true);
    $locationProvider.html5Mode({
	  enabled: true,
	  requireBase: false
	});
}])

