angular.module('app.routes', ['ngRoute', 'ngAnimate'])

.config(function($routeProvider) {

	$routeProvider

		// route for the home page
		.when('/', {
			templateUrl : 'views/dashboard.html',
			controller: 'dashboardController',
			controllerAs: 'dash'
		})
		
		.when('/tweets', {
			templateUrl: 'views/annotate.html',
			controller: 'tweetController',
			controllerAs: 'tweet'
		});
	


});
