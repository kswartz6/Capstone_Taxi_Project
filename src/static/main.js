

var daysInMonth ={
	1:31,
	2:28,
	2.5:29,
	3:31,
	4:30,
	5:31,
	6:30,
	7:31,
	8:31,
	9:30,
	10:31,
	11:30,
	12:31
}


var map = L.map('map', {drawControl: true}).setView([40.727, -73.976], 12);

//Hey, so this is shitty. It'll go away and be replaced with local vars later.
//For now we'll use this global variable for testing purposes.
var testRecord = {};


var app = angular.module("app", []);

//Jinja2 and angular don't play well since they have the same syntax.
//Ergo we change interpolation of ngDirectives to be curly brace, regular brace
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);


//controller for mapView
app.controller("mapView", function($scope,$http) {
	$scope.currentDateTime      = {};
	$scope.currentDateTime.MM   = 1;
	$scope.currentDateTime.DD   = 1;
	$scope.currentDateTime.YYYY = 2013


	$scope.dateTimeIncre = function(arg){
		var i = $scope.currentDateTime[arg];
		switch (true) {
			case (arg == "DD"):
				j = $scope.currentDateTime.MM;
				if(j == 2 && ($scope.currentDateTime.YYYY % 4) == 0){
					j = 2.5;
				}

				if(i == daysInMonth[j]){
					i = 1;
				} else {
					i += 1;
				}
				break;
			case (arg == "MM"):
				if(i == 12){
					i = 1;
				} else {
					i += 1;
				}
				break;
			default:
				i += 1;
		}
		$scope.currentDateTime[arg] = i;
	}

	$scope.dateTimeDecre = function(arg){
		var i = $scope.currentDateTime[arg];
		switch (true) {
			case (arg == "DD"):
				if(i == 1){
					j = $scope.currentDateTime.MM;
					if(j == 2 && ($scope.currentDateTime.YYYY % 4) == 0){
						j = 2.5;
					}
					i = daysInMonth[j];
				} else {
					i -= 1;
				}
				break;
			case (arg == "MM"):
				if(i == 1){
					i = 12;
				} else {
					i -= 1;
				}
				break;
			default:
				i -= 1;
		}
		$scope.currentDateTime[arg] = i;
	}

	//Setting up the test api call here.
	//This is an async call, so testResponse acts as a promised value.
	var testResponse = $http.get("/api/test")
	testResponse.success(function(data, status, headers, config) {
    console.log(data);
		testRecord = data;
		console.log(testRecord);
  });

	var TeeHee = {"pickup_longitude": -73.980072,
						    "pickup_latitude": 40.743137,
						    "dropoff_longitude": -73.982712,
						    "dropoff_latitude": 40.735336}

	var testStructure = $http({
																url:"/api/structure",
																method: "GET",
																params: TeeHee })
	testStructure.success(function(data, status, headers, config) {
    console.log(data);
		testRecord = data;
		console.log(testRecord);
  });


});



L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	maxZoom: 18,
	minZoom: 10,
    	id: 'cschaufe.n9je0n8b',
    	accessToken: 'pk.eyJ1IjoiY3NjaGF1ZmUiLCJhIjoiMTI1OWU4Y2FjZTgwNzE5MGFmMGRjMjc4MzQxOTRlMDgifQ.KFvjasOmW-nyz90HQktgPg'
}).addTo(map);


// Initialise the FeatureGroup to store editable layers
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems
    }
});


//add draw function
map.on('draw:created', function (e) {
    var type = e.layerType,
        layer = e.layer;

    if (type === 'marker') {
        // Do marker specific actions
    }

    // Do whatever else you need to. (save to db, add to map etc)
    map.addLayer(layer);
});
