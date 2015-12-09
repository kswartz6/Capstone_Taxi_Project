import pymongo
from bson.json_util import dumps
import ast
from bson.son import SON
from datetime import *

MONGO_DB_URI = "mongodb://localhost:27017"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.csf2015capstone

def cleanupDate(document):
	pickup_date = document["pickup_datetime"]
	dropoff_date = document["dropoff_datetime"]
	if(pickup_date != None):
		index_to_replace = pickup_date.find(" ")
		pickup_date = list(pickup_date)
		pickup_date[index_to_replace] = "T"
		pickup_date = "".join(pickup_date)
		pickup_date = pickup_date + ":000Z"
		pickup = {
			'date' : pickup_date
		}
		document.pop("pickup_datetime")
		document["pickup_datetime"] = pickup

	if(dropoff_date != None):
		index_to_replace = dropoff_date.find(" ")
		dropoff_date = list(dropoff_date)
		dropoff_date[index_to_replace] = "T"
		dropoff_date = "".join(dropoff_date)
		dropoff_date = dropoff_date + ":000Z"
		dropoff = {
		'date' : dropoff_date
		}
		document.pop("dropoff_datetime")
		document["dropoff_datetime"] = dropoff

		pickup_date = datetime.strptime(document["pickup_datetime"]["date"], "%Y-%m-%dT%H:%M:%S:%fZ")
		dropoff_date = datetime.strptime(document["dropoff_datetime"]["date"], "%Y-%m-%dT%H:%M:%S:%fZ")

		document["pickup_datetime"]["date"] = pickup_date
		document["dropoff_datetime"]["date"] = dropoff_date

		return document

def cleanupData():
	cursor = db.taxitest.find()
	current_doc_number = 1
	for document in cursor :
		if(("pickup_longitude" in document) != True):
			current_doc_number += 1
			print("Skipping: " + str(current_doc_number))
			continue

		print("currently updating: " + str(current_doc_number))
		pickup_long = document["pickup_longitude"]
		pickup_lat = document["pickup_latitude"]
		dropoff_long = document["dropoff_longitude"]
		dropoff_lat = document["dropoff_latitude"]

		pickup_coord = [pickup_long, pickup_lat]
		dropoff_coord = [dropoff_long, dropoff_lat]

		pickup = {
			'loc' : pickup_coord
		}

		dropoff = {
			'loc' : dropoff_coord
		}

		document["pickup_loc"] =  pickup
		document["dropoff_loc"] =  dropoff
		document.pop("pickup_longitude")
		document.pop("pickup_latitude")
		document.pop("dropoff_longitude")
		document.pop("dropoff_latitude")
		document = cleanupDate(document)
		db.taxitest.update({"_id":document["_id"]}, document, True)
		print("done updating: " + str(current_doc_number))
		current_doc_number += 1

def clearnupOutOfRangePoints() :
	cursor = db.taxitest.find()
	current_doc = 1
	for document in cursor :
		if(not("pickup_loc" in document.keys()) or not("dropoff_loc" in document.keys())) :
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue
		pickup = list(document["pickup_loc"]["loc"])
		dropoff = list(document["dropoff_loc"]["loc"])
		print("Currently looking at document: " + str(current_doc))
		current_doc += 1
		if(pickup == None or dropoff == None) :
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue
		if(isinstance(pickup[0], str) or isinstance(pickup[1], str) or isinstance(dropoff[0], str) or isinstance(dropoff[1], str)):
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue
		if (float(pickup[0]) < -100 or float(pickup[1]) > 100) :
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue
		if (float(dropoff[0]) < -100 or float(dropoff[1]) > 100) :
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue
		if(float(pickup[0]) > 100 or float(pickup[1]) < 25) :
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue
		if(float(dropoff[0]) > 100 or float(dropoff[1]) < 25) :
			print("removing record: " + str(current_doc - 1) + " with _id: " + str(document["_id"]))
			db.taxitest.remove(document["_id"])
			continue

def buildIndexes() :
	print("Currently creating geospatial indexing on pickup_loc")
	db.taxitest.create_index([("pickup_loc.loc",pymongo.GEO2D), ('pickup_datetime.date', pymongo.ASCENDING)])

	print("Currently creating geospatial indexing on dropoff_loc")
	db.taxitest.create_index([("dropoff_loc.loc",pymongo.GEO2D), ('dropoff_datetime.date', pymongo.ASCENDING)])

cleanupData()
clearnupOutOfRangePoints()
buildIndexes()