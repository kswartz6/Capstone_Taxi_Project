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


var app = angular.module("app", []);

//Jinja2 and angular don't play well since they have the same syntax.
//Ergo we change interpolation of ngDirectives to be curly brace, regular brace
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);


//controller for mapView
app.controller("mapView", function($scope,$http, $timeout) {
	$scope.currentDateTime      = {};
	$scope.currentDateTime.MM   = 3;
	$scope.currentDateTime.DD   = 1;
	$scope.currentDateTime.YYYY = 2013;
	$scope.currentDateTime.hours = 0;
	$scope.currentDateTime.minutes = 21;
	$scope.currentDateTime.seconds = 53;
	updateDateTime();

	function updateDateTime(){
		var min = $scope.currentDateTime.minutes.toString();
		var hrs = $scope.currentDateTime.hours.toString();
		var sec = $scope.currentDateTime.seconds.toString();
		var month = $scope.currentDateTime.MM.toString();
		var days = $scope.currentDateTime.DD.toString();

		$scope.currentDateTime.formatted = $scope.currentDateTime.YYYY;
		$scope.currentDateTime.formatted += ',' + month;
		$scope.currentDateTime.formatted += ',' + days;
		$scope.currentDateTime.formatted += ',' + hrs;
		$scope.currentDateTime.formatted += ',' + min;
		$scope.currentDateTime.formatted += ',' + sec;
		console.log($scope.currentDateTime.formatted)
	}

	$scope.collections = [];
	$scope.play = false;
	//playState is the state of time playback





	var testResponse = $http.get("/api/test")
	testResponse.success(function(data, status, headers, config) {
		console.log(data);
		testRecord = data;
		console.log(testRecord);
		 //http://leafletjs.com/examples/custom-icons.html
		//
	});

	var TeeHee = {"pickup_longitude": -73.980072,
								"pickup_latitude": 40.743137,
								"dropoff_longitude": -73.982712,
								"dropoff_latitude": 40.735336}

	var testStructure = $http({		url:"/api/structure",
																method: "GET",
																params: TeeHee })

	testStructure.success(function(data, status, headers, config) {
		console.log(data);
		testRecord = data;
		console.log(testRecord);
		var iconSize = [6, 6];
		var blueIcon = L.icon({
			iconUrl: '/static/images/circle-blue.png',
			iconSize: iconSize
			});
		/*geoJson not showing on map*/
		//L.geoJson(geojsonFeature).addTo(map); g
		L.marker([data[0].dropoff_loc.loc[0], data[0].dropoff_loc.loc[1]], {icon: blueIcon}).addTo(map);
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
		var polygonRefID = $scope.collections.length;
		var bounds = (layer.getLatLngs());
		console.log(bounds);

		//TODO: GET RID OF THIS SHITTY QUERY method
		//NO SERIOUSLY THIS IS SHIT AND I FEEL BAD FOR DOING IT LIKE THIS
		var jankyString = "";
		for (i in bounds){
			console.log(i);
			jankyString += bounds[i].lng + ',' + bounds[i].lat;
			jankyString += '|'
		}
		jankyString = jankyString.substring(0, jankyString.length - 1);
		//Get rid of the damn last pipe
		console.log(jankyString);
		map.addLayer(layer);

		if(type === 'rectangle'){
		} else if(type === 'polygon'){
			console.log(bounds);
		}

		$scope.$apply(function() {
			$scope.collections.push({obj: layer, index: polygonRefID});
			layer.markers = [];
			var newtestStructure = $http({		url:"/api/structure",
			method: "GET",
			params: {"bounds": jankyString,
							 "datetime": $scope.currentDateTime.formatted} })
			newtestStructure.success(function(data, status, headers, config) {
				console.log("success!")
				console.log(data);
				var layerColl = [];
				for (i = 0; i < data.length; ++i){
						var testIcon = L.icon({
								iconUrl: 'static/images/BlueMarker.png',
								iconSize: [4, 4],
						});
						layerColl.push(L.marker([data[i].pickup_loc.loc[1], data[i].pickup_loc.loc[0]], {icon: testIcon}));
				}
				layer.markers = L.layerGroup(layerColl).addTo(map);
			});
		});
		console.log($scope.collections);
	});


	//Polygon delete function
	$scope.deletePolygon = function(e){
		$scope.collections.splice(e.index, 1)
		console.log($scope.collections);
		console.log(e.obj);
		window.map.removeLayer(e.obj.markers);
		window.map.removeLayer(e.obj);

	}

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
			case (arg == "YYYY"):
				if(i == 2013){
					i = 2014
				} else {
					i = 2013
				}
				break;
				case (arg == "hours"):
					if (i == 00){
						i = 1;
					} else if (i == 23){
						$scope.dateTimeIncre("DD");
						i += 1;
					} else {
						i += 1;
					}
					break;
				case (arg == "minutes"):
					if (i == 59){
						i = 0;
						$scope.dateTimeIncre("hours");
					} else {
						i += 1;
					}
					break;
				case (arg == "seconds"):
					if (i == 59){
						i = 0;
						$scope.dateTimeIncre("minutes");
					} else {
						i += 1;
					}
					break;
			default:
				i += 1;
		}
		$scope.currentDateTime[arg] = i;
		updateDateTime();
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
			case (arg == "hours"):
				if (i == 1){
					i = 0;
				} else if (i == 0){
					$scope.dateTimeDecre("DD");
					i -= 1;
				} else {
					i -= 1;
				}
				break;
			case (arg == "minutes"):
				if (i == 0){
					i = 59;
					$scope.dateTimeDecre("hours");
				} else {
					i -= 1;
				}
				break;
			case (arg == "seconds"):
				if (i == 0){
					i = 59;
						$scope.dateTimeDecre("minutes");
				} else {
					i -= 1;
				}
				break;
			default:
				i -= 1;
		}
		$scope.currentDateTime[arg] = i;
		updateDateTime();
	}


	$scope.ff = function(){
		$timeout.cancel($scope.timeout);
		fastforward();
	}

	$scope.rw = function(){
		$timeout.cancel($scope.timeout);
		rewind();
	}

	$scope.startPlay = function(){
		if ($timeout != undefined){
			$timeout.cancel($scope.timeout);
		}
		countdownPlayState();
	}

	$scope.pausePlay = function(){
			$timeout.cancel($scope.timeout);
	}

	function countdownPlayState(){
		$scope.dateTimeIncre("seconds")
		$scope.timeout = $timeout(countdownPlayState, 1000);
	}

	function fastforward(){
		$scope.dateTimeIncre("seconds")
		$scope.timeout = $timeout(fastforward, 50);
	}

	function rewind(){
		$scope.dateTimeDecre("seconds")
		$scope.timeout = $timeout(rewind, 50);
	}


});
