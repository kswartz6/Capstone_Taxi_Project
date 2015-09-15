import os
import sys
import logging
import json
import pymongo
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session

MONGO_DB_URI = "mongodb://bob:bob@ds051368.mongolab.com:51368/taxitest"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.get_default_database()



webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')



#API Routes
#General format is "/api/<endpoint here>"


@webapp.route("/api/test")
def api_test():
	data = { 'test1':'42','test2':3}
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

#server initializiation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port, debug=True)
