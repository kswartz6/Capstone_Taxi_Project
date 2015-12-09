import os
import sys
import logging
import json
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session
from controller.query import *

webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')

# API Routes
# General format is "/api/<endpoint here>"
@webapp.route("/api/structure")
def api_structure():
	geometryType = request.args["type"]
	bounds = request.args["bounds"]
	formatDT = request.args["datetime"].split(",")

	if(geometryType == "rectangle" or geometryType == "polygon"):
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
	else:
		print("CIRCLE")
		bounds = bounds.split(",")
		tmp = bounds;
		bounds = [[float(tmp[0]), float(tmp[1])], float(tmp[2])/6378100]

	q = {}
	q["bounds"] = bounds;
	q["p_dt"] = formatDT

	if(geometryType == "rectangle" or geometryType == "polygon"):
		cursor = polygonQuery(q, True)
		print("Received cursor")
		return cursor
	elif(geometryType == "circle"):
		cursor = circleQuery(q, True)
		print("Received cursor")
		return cursor

#server initializiation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port, debug=True)
