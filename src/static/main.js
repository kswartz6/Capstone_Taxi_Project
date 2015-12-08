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


var map = L.map('map', {drawControl: false}).setView([40.727, -73.976], 12);
var svg = d3.select(map.getPanes().overlayPane).append("svg"),
    g = svg.append("g").attr("class", "leaflet-zoom-hide");

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
	$scope.currentDateTime.DD   = 25;
	$scope.currentDateTime.YYYY = 2013;
	$scope.currentDateTime.hours = 8;
	$scope.currentDateTime.minutes = 29;
	$scope.currentDateTime.seconds = 59;
	$scope.currentDateTime.dateTimer = new Date(
		$scope.currentDateTime.YYYY,
		$scope.currentDateTime.MM - 1,
		$scope.currentDateTime.DD,
		$scope.currentDateTime.hours - 5,
		$scope.currentDateTime.minutes,
		$scope.currentDateTime.seconds
	).getTime()


	updateDateTime();

	function updateDateTime(){
		var min = $scope.currentDateTime.minutes.toString();
		var hrs = $scope.currentDateTime.hours.toString();
		var sec = $scope.currentDateTime.seconds.toString();
		var month = $scope.currentDateTime.MM.toString();
		var days = $scope.currentDateTime.DD.toString();
		$scope.currentDateTime.dateTimer = new Date(
			$scope.currentDateTime.YYYY,
			$scope.currentDateTime.MM - 1,
			$scope.currentDateTime.DD,
			$scope.currentDateTime.hours,
			$scope.currentDateTime.minutes,
			$scope.currentDateTime.seconds
		).getTime()
		var x = $scope.currentDateTime.dateTimer
		console.log(x)
		$scope.currentDateTime.formatted = $scope.currentDateTime.YYYY;
		$scope.currentDateTime.formatted += ',' + month;
		$scope.currentDateTime.formatted += ',' + days;
		$scope.currentDateTime.formatted += ',' + hrs;
		$scope.currentDateTime.formatted += ',' + min;
		$scope.currentDateTime.formatted += ',' + sec;

		for (n in $scope.collections){
			collection = $scope.collections[n]
			console.log(collection.obj.markers.toGeoJSON())
			console.log(collection)
			if (typeof collection.dropoffs[x] == "undefined"){
			} else {
				//Removing locations
				for (var i = 0; i < collection.dropoffs[x].length; i++){
					var tmp = collection.dropoffs[x][i]
					if (collection.obj.markers.hasLayer(tmp.dropoff)){
						collection.obj.markers.removeLayer(tmp.dropoff)
						for (var j = 0; j < collection.pickups[tmp.removeTime].length; j++){
							var pick = collection.pickups[tmp.removeTime][j]
							if (pick.removeTime == x){
								collection.actives[pick.index] = null
								actives[collection.index] = collection.actives
								collection.obj.markers.removeLayer(pick.pickup)
							}
						}
					}
				}
			}

			//Adding locations
			if (typeof collection.pickups[x] == "undefined"){
			} else {
				for (i in collection.pickups[x]){
					collection.obj.markers.addLayer(collection.pickups[x][i].pickup)
					collection.actives[collection.pickups[x][i].index] = collection.pickups[x][i]
					actives[collection.index] = collection.actives
					var correspond = collection.dropoffs[collection.pickups[x][i].removeTime]
					for (j in correspond)
						if (correspond[j].removeTime == x){
							collection.obj.markers.addLayer(correspond[j].dropoff)
						}
					}
			}
			console.log(actives)
			UpdateChart(actives)
			tweenPoints()
		}
	}

	function tweenPoints(){

	}


	$scope.filterPoints = function(e){
		filterforCollection(e)
	}

	function filterforCollection(e){
		console.log("Fired filter function")
		for(i in actives[e.index]){
			if(actives[e.index][i] != null){
				if(checkInFilter(e, e.filter, actives[e.index][i].dropoff._latlng)){
					if (!e.obj.markers.hasLayer(actives[e.index][i].dropoff)){
						e.obj.markers.addLayer(actives[e.index][i].dropoff)
					}
					if (!e.obj.markers.hasLayer(actives[e.index][i].pickup)){
						e.obj.markers.addLayer(actives[e.index][i].pickup)
					}
				} else {
					if (e.obj.markers.hasLayer(actives[e.index][i].dropoff)){
						e.obj.markers.removeLayer(actives[e.index][i].dropoff)
					}
					if (e.obj.markers.hasLayer(actives[e.index][i].pickup)){
						e.obj.markers.removeLayer(actives[e.index][i].pickup)
					}
				}
			}
		}
	}

//statenIsland, bronx, queens, brooklyn, manhattan;
	function checkInFilter(e, label, point){
		var inFilter = false
		switch (label){
			case	"None":
					inFilter = true
					break
			case	"Self":
					leafletPip.pointInLayer(point, e, true)
						inFilter = true
					break
			case  "Manhattan":
					if(!manhatt) {
						addBoroughToMap(3);
					}
					manhatt = true;
					console.log(leafletPip.pointInLayer(point, boroughLayer.manhattan.obj, true).length)
					if(leafletPip.pointInLayer(point, boroughLayer.manhattan.obj, true).length > 0)
						inFilter = true
					break
			case	"Brooklyn":
					if(!brook) {
						addBoroughToMap(2);
					}
					brook = true;

					if(leafletPip.pointInLayer(point, boroughLayer.brooklyn.obj, true).length > 0)
						inFilter = true
					break;
			case	"Queens":
					if(!queen) {
						addBoroughToMap(1);
					}
					queen = true;
					if(leafletPip.pointInLayer(point, boroughLayer.queens.obj, true).length > 0)
						inFilter = true
					break;
			case	"Bronx":
					if(!bron) {
						addBoroughToMap(4);
					}
					bron = true;
					if(leafletPip.pointInLayer(point, boroughLayer.bronx.obj, true).length > 0)
						inFilter = true
					break;
			case	"Staten Island":
					if(!staten) {
						addBoroughToMap(0);
					}
					staten = true;
					if(leafletPip.pointInLayer(point, boroughLayer.statenIsland.obj, true).length > 0)
						inFilter = true
					break;
			case  "Custom":
					if(!e.obj.custom) {
						addCustomToMap();
					}
					e.obj.custom = true
				break;
			default:
		}
	}


	function projectPoint(x, y) {
  	var point = map.latLngToLayerPoint(new L.LatLng(y, x));
  	this.stream.point(point.x, point.y);
	}

	var transform = d3.geo.transform({point: projectPoint}),
    path = d3.geo.path().projection(transform);

	// var feature = g.selectAll("path")
	//      					 .data()
	//                .enter().append("path");


	$scope.collections = [];
	$scope.collectionFilters = [
		"None",
		"Self",
		"Manhattan",
		"Brooklyn",
		"Queens",
		"Bronx",
		"Staten Island",
		"Custom"
	]

	$scope.play = false;
	var actives = []




	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
		minZoom: 10,
	    	id: 'cschaufe.n9je0n8b',
	    	accessToken: 'pk.eyJ1IjoiY3NjaGF1ZmUiLCJhIjoiMTI1OWU4Y2FjZTgwNzE5MGFmMGRjMjc4MzQxOTRlMDgifQ.KFvjasOmW-nyz90HQktgPg'
	}).addTo(map);

	defautPolyColor = '#feffa3';

	// Initialise the FeatureGroup to store editable layers
	var drawnItems = new L.FeatureGroup();
	map.addLayer(drawnItems);


	// Initialise the draw control and pass it the FeatureGroup of editable layers
	var drawControl = new L.Control.Draw({
		position: 'topleft',
		draw: {
			polygon: {
				shapeOptions: {
					color: defautPolyColor
				},
				allowIntersection: false,
				drawError: {
					color: 'orange',
					timeout: 1000
				},
				showArea: true,
				metric: false,
				repeatMode: true
			},
			polyline: {
				shapeOptions: {
					color: defautPolyColor
				},
			},
			rectangle: {
				shapeOptions: {
					color: defautPolyColor
				},
			},
			circle: {
				shapeOptions: {
					color: defautPolyColor
				},
			},
		},
		edit: {
			featureGroup: drawnItems
		}
	});




map.addControl(drawControl);

	//add draw function
	map.on('draw:created', function (e) {
		//window.polygon.setStyle({fillColor: '#dddddd'});
		var type = e.layerType,
		layer = e.layer;
		var polygonRefID = $scope.collections.length;
		var pointString = "";

		if(type === 'rectangle' || type === 'polygon'){
			var bounds = (layer.getLatLngs());
			console.log(bounds);
			for (i in bounds){
				console.log(i);
				pointString += bounds[i].lng + ',' + bounds[i].lat;
				pointString += '|'
			}
			pointString = pointString.substring(0, pointString.length - 1);
		} else if(type === 'circle') {
			var latLng = layer.getLatLng();
			pointString += latLng.lng + ',' + latLng.lat + ',' + layer.getRadius();
		}
		//Get rid of the last pipe
		console.log(pointString);
		map.addLayer(layer);

		$scope.$apply(function() {
			layer.markers = [];
			var newtestStructure = $http({		url:"/api/structure",
			method: "GET",
			params: {"bounds": pointString,
							 "datetime": $scope.currentDateTime.formatted,
							 "type": type} })
			newtestStructure.success(function(data, status, headers, config) {
				console.log("success!")
				console.log(data);
				var pickColl = {};
				var dropColl = {};
				layer.markers = L.layerGroup([]).addTo(map);
				for (i = 0, l = data.length; i < l; ++i){
						var pickIcon = L.icon({
								iconUrl: 'static/images/BlueMarker.png',
								iconSize: [4, 4],
						});
						var dropIcon = L.icon({
								iconUrl: 'static/images/RedMarker.png',
								iconSize: [4, 4],
						});
						var pickup = L.marker([data[i].pickup_loc.loc[1], data[i].pickup_loc.loc[0]], {icon: pickIcon})
						var dropoff = L.marker([data[i].dropoff_loc.loc[1], data[i].dropoff_loc.loc[0]], {icon: dropIcon})
						var dropLocName = data[i].dropoff_datetime.date.$date
						var pickLocName = data[i].pickup_datetime.date.$date

						var dropLoc = {};
						dropLoc.dropoff = dropoff;
						dropLoc.removeTime = data[i].pickup_datetime.date.$date

						//Because pickups are used for determining plotting, we'll
						//associate data to this object.
						var pickLoc = {}
						pickLoc.pickup = pickup
						pickLoc.removeTime = data[i].dropoff_datetime.date.$date
						pickLoc.index = i
						pickLoc.data = data[i]


						if (pickColl[pickLocName] === undefined){
							pickColl[pickLocName] = [];
						}
						pickColl[pickLocName].push(pickLoc);

						if (dropColl[dropLocName] === undefined){
							dropColl[dropLocName] = [];
						}
						dropColl[dropLocName].push(dropLoc);
					}
				$scope.collections.push({obj: layer, index: polygonRefID, pickups:pickColl, dropoffs:dropColl, actives:{}});
				createBar(actives);
				updateDateTime()
				console.log($scope.collections);
			});
		});


	});



	//marker remove function
	function removeMarker(e){
		window.map.removeLayer(e);
	}

	//Polygon delete function
	$scope.deletePolygon = function(e){
		actives.splice($scope.collections.indexOf(e), 1);
		$scope.collections.splice($scope.collections.indexOf(e), 1);
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
					if (i == 0){
						i = 1;
					} else if (i == 23){
						$scope.dateTimeIncre("DD");
						i = 0;
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
					i = 23;
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
		$scope.timeout = $timeout(countdownPlayState, 250);
	}

	function fastforward(){
		$scope.dateTimeIncre("seconds")
		$scope.timeout = $timeout(fastforward, 10);
	}

	function rewind(){
		$scope.dateTimeDecre("seconds")
		$scope.timeout = $timeout(rewind, 10);
	}

	$scope.clearBoroughs = function() {
		boroughLayer.clearLayers();
		bron = false;
		manhatt = false;
		staten = false;
		brook = false;
		queen = false;
	}

	$scope.mapStaten = function() {
		if(!staten) {
			addBoroughToMap(0);
		}
		staten = true;

	}
	$scope.mapQueens = function(){
		if(!queen) {
			addBoroughToMap(1);
		}
		queen = true;
	}
	$scope.mapBrooklyn = function() {
		if(!brook) {
			addBoroughToMap(2);
		}
		brook = true;
	}
	$scope.mapManhattan = function() {
		if(!manhatt) {
			addBoroughToMap(3);
		}
		manhatt = true;
	}
	$scope.mapBronx = function() {
		if(!bron) {
			addBoroughToMap(4);
		}
		bron = true;
	}
	// These are holding all of our borough geoJson data
	var statenIsland, bronx, queens, brooklyn, manhattan;

	// These are bools that allow us to check for multiple drawing of boroughs in leaflet
	var staten = false, bron = false, queen = false, brook = false, manhatt = false;

	function loadBoroughs() {
		var boroFile;
		$.getJSON('/static/boroughs.geojson', function(data) {
    		boroFile=data;
  		}).done(function(){
  			console.log("Loaded Borough JSON")
  			statenIsland = boroFile["features"][0];
  			queens = boroFile["features"][1];
  			brooklyn = boroFile["features"][2];
  			manhattan = boroFile["features"][3];
  			bronx = boroFile["features"][4];
  			console.log("Borough Coordinates have been loaded");
  		});

	}
	var boroughLayer = L.geoJson();
	boroughLayer.addTo(map);

	function addBoroughToMap(boroughNumber) {
		switch(boroughNumber){
			case 0:
				boroughLayer.addData(statenIsland);
				break;
			case 1:
				boroughLayer.addData(queens);
				break;
			case 2:
				boroughLayer.addData(brooklyn);
				break;
			case 3:
				boroughLayer.addData(manhattan);
				break;
			case 4:
				boroughLayer.addData(bronx);
				break;
		}
	}

	function reverseBoroughLongLat(borough) {
		for(var i = 0; i < borough.length; ++i) {
  			for(var j = 0; j < borough[i].length; ++j) {
  				for(var k = 0; k < borough[i][j].length; ++k){
  					var temp = borough[i][j][k][0];
  					borough[i][j][k][0] = borough[i][j][k][1];
  					borough[i][j][k][1] = temp;
  				}
  			}
  		}
  		return borough;
	}

	loadBoroughs();
});
