import os
import sys
import logging
import json
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session
from controller.query import *








#for keys, values in json.items():
 #   print(keys)
  #  print(values)
#print(json)

webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')



# API Routes
# General format is "/api/<endpoint here>"


@webapp.route("/api/structure")
def api_structure():
	bounds = request.args["bounds"]
	bounds = bounds.split("|")
	tmp = bounds;
	bounds = [];
	for pair in tmp:
		i = pair.split(",")
		tmp2 = i;
		i = [];
		for j in tmp2:
			j = float(j)
			i.append(j)
		bounds.append(i)
	q = {}
	q["bounds"] = bounds;
	q["p_dt"] = request.args["datetime"]
	cursor = mongoQuery(q)
	# js = json.dumps(cursor.collection)
	# resp = Response(js, status=200, mimetype='application/json')
	# return resp
	return cursor


@webapp.route("/api/test")
def api_test():
	data = {
    "_id": {
        "$oid": "55f7957923178c92ee25df83"
    },
    "medallion": "2C0E91FF20A856C891483ED63589F982",
    "hack_license": "1DA2F6543A62B8ED934771661A9D2FA0",
    "vendor_id": "CMT",
    "rate_code": 1,
    "store_and_fwd_flag": "N",
    "pickup_datetime": "2013-01-07 18:15:47",
    "dropoff_datetime": "2013-01-07 18:20:47",
    "passenger_count": 1,
    "trip_time_in_secs": 299,
    "trip_distance": 0.8,
    "pickup_longitude": -73.980072,
    "pickup_latitude": 40.743137,
    "dropoff_longitude": -73.982712,
    "dropoff_latitude": 40.735336 }

	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

#server initializiation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port, debug=True)
