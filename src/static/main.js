

var map = L.map('map').setView([40.727, -73.976], 12);

//Hey, so this is shitty. It'll go away and be replaced with local vars later.
//For now we'll use this global variable for testing purposes.
var testRecord = {};


var app = angular.module("app", []);

//controller for mapView
app.controller("mapView", function($scope,$http) {

	//Setting up the test api call here.
	var testResponse = $http.get("/api/test")
	testResponse.success(function(data, status, headers, config) {
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
