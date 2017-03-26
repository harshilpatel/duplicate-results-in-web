var app = angular.module('app', ['ngRoute', 'ngAnimate', 'ngResource'])

app.factory('QUERY', function($resource){
    return $resource('/tool/search');
})

app.factory('history', function($resource){
    return $resource('/history');
})

app.controller('search', function($scope, QUERY, history){
    $scope.query = "";
    $scope.queryQuantity = 30;
    $scope.queryForce = false;
    $scope.results = [];
    $scope.focusedResult = "";
    $scope.filterKeywords = [];
    $scope.history = history.query();

    $scope.search = function(){
        $("#submitQuery").removeClass('btn-danger');
        if($scope.query.length > 0){
            // $("#submitQuery").attr('disabled', 'disabled');
            $("#submitQuery").addClass('btn-warning');
            $scope.results = QUERY.query({query:$scope.query,
                                        quantity:$scope.queryQuantity,
                                        force:$scope.queryForce,
                                            }, function(){
                                                // $("#submitQuery").removeAttr('disabled');
                                                $("#submitQuery").removeClass('btn-warning');
                                                $("#submitQuery").addClass('btn-success');
                                            });
            console.clear();
        } else{
            $("#submitQuery").addClass('btn-danger');
        }
    }

    $scope.focusResult = function(r){
        $scope.focusedResult = angular.copy(r);
    }

    $scope.filterByKeyword = function($event,text){

        // $scope.filterKeywords = $scope.filterKeywords.split(" ");

        if($scope.filterKeywords.indexOf(text) == -1){
            $scope.filterKeywords.push(text);
        } else{
            $scope.filterKeywords.splice($scope.filterKeywords.indexOf(text), 1);
        }
        console.log($scope.filterKeywords);

        $($event.target).toggleClass('btn-success');


        angular.forEach($scope.results, function(result, index){
            result.hide = false;
            if(result.text){
                angular.forEach($scope.filterKeywords, function(key){
                    var index = result.text.indexOf(key);
                    if(index == -1){
                        result.hide = true;
                        // break;
                    }

                })
            }
        })
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