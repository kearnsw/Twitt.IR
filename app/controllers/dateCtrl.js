angular.module('dateSlider', ['dashboard'])
.controller('dateController', function($scope, activeDate) {

$scope.$watch('dateValue', function(newValue){
        console.log(newValue);
        activeDate.setDate(newValue)
    });

});