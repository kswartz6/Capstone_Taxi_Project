import os
import sys
import logging
import json
import pymongo
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, session

MONGO_DB_URI = "mongodb://bob:bob@ds051368.mongolab.com:51368/taxitest"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.get_default_database()



webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port)
