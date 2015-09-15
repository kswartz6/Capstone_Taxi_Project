import os
import sys
import logging
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, session
from pymongo import MongoClient, Connection

MONGO_DBC = "ds051368.mongolab.com"
MONGO_PORT = 51368
connection = MongoClient(MONGO_DBC, MONGO_PORT)
db = connection["taxitest"]
db.authenticate("admin","admin")

webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port)
