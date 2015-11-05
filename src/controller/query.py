import pymongo
from bson.json_util import dumps
import ujson
import ast
from bson.son import SON
from datetime import *

MONGO_DB_URI = "mongodb://bob:bob@ds051368.mongolab.com:51368/csf2015capstone"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.csf2015capstone
#returns cursor object for now. We do processing of documents in cursor within other
#functions?
#queryRequest should ALWAYS contain p_dt and bounds
#pdt = pickup date time
#bounds = coord points of polygon on leaflet
#bounds MUST be an iterable of iterables such that [ [x1, y1], [x2, y2] ]



def decompose(dt):
	dt = {}
	dt["d"] = queryRequest["p_dt"]
	dt["d"] = datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))
	dt["ud"] = d + timedelta(hours=1)
	dt["ld"] = d + timedelta(hours= -1)
	return dt


def mongoQuery(queryRequest):
	print(queryRequest["bounds"])
	print(type(queryRequest["bounds"]))
	d = queryRequest["p_dt"]
	d = datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))
	ud = d + timedelta(hours=1)
	ld = d + timedelta(hours= -1)
	#"pickup_datetime.date":d is the pickup query param
	# cursor = db.taxitest.find({ 'pickup_loc.loc' : { '$geoNear' : [-73.980072, 40.743137]}}).limit(5)
	print("Launching find")
	cursor = db.taxitest.find({"pickup_datetime.date":{"$gt":ld,"$lt":ud},
	"pickup_loc.loc":{"$geoWithin": {"$polygon": queryRequest["bounds"]}}
	},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)
	print("Dumping Cursor")
	return dumps(cursor)

	#db.taxitest.create_index({"pickup_loc.loc", pymongo.GEO2D})
	#db.taxitest.create_index({"dropoff_loc.loc", pymongo.GEO2D})


	#argsString = ""
	#firstFlag = True;
#
	#db.taxitest.get_indexes()
#
	#for key in queryRequest:
	#	print(key)
	##	pickup_longitude": -73.980072,
	##					    "pickup_latitude": 40.743137,
	#	if(firstFlag):
	#		argsString = "{'$geometry':{'" + key + "':{'$near' :[" + queryRequest[key] + "]}"
	#		firstFlag = False;
	#argsString = "{'pickup_loc':{'$near':{'$geometry':{'type':'Point', 'coordinates' : [-73.980072, 40.743137]},"
	#argsString += "'$maxDistance':100000, '$minDistance':0}}}"
	#
	#print(argsString)
	#qString = ast.literal_eval({{"pickup_loc": {"$near": [-73.980072, 40.743137]}}})
	#cursor = db.taxitest.find({ 'dropoff_loc.loc' : { '$geoNear' : [-73.980072, 40.743137]}}).limit(5)
#	SON([("$near", [-73.980072, 40.743137]), ("$maxDistance", 100)]

	#print("hello")
	#for document in cursor :
	#	print(document)
		#db.taxitest.
#
	#return 1
#	below is sample query for a given location
# 	cursor = db.taxitest.find({"pickup_loc" : { "loc" : {"$near": [-73.980072, 40.743137]}}}).limit(3)


#bulkQuery grabs 100 records
def bulkQuery():
	cursor = db.taxitest.find().limit(100)
	return cursor


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
		return document



def cleanupData():
	cursor = db.taxitest.find()
	current_doc_number = 1
	for document in cursor :
		if(current_doc_number <= 438409):
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

	print("Currently creating geospatial indexing on pickup_loc")
	#db.taxitest.create_index({"pickup_loc.loc", pymongo.GEO2D})

	print("Currently creating geospatial indexing on dropoff_loc")
	#db.taxitest.create_index({"dropoff_loc.loc", pymongo.GEO2D})

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
#	#cursor = db.taxitest.find().limit(5)
#	#for document in cursor :
#	#	print(document)
	print("Currently creating geospatial indexing on pickup_loc")
	db.taxitest.create_index([("pickup_loc.loc",pymongo.GEO2D),("pickup_datetime.date",pymongo.ASCENDING)])

	print("Currently creating geospatial indexing on dropoff_loc")
	db.taxitest.create_index([("dropoff_loc.loc",pymongo.GEO2D),("dropoff_datetime.date",pymongo.ASCENDING)])

def printAllDocs():
	#cursor = db.taxitest.find({ 'pickup_loc.loc' : { '$geoNear' : [-73.980072, 40.743137]}}).limit(5)
	#db.taxitest.create_index([("dropoff_loc.loc", pymongo.GEO2D)])
	cursor = db.taxitest.find()
	index = 1
	for document in cursor :
		if(index <= 596299) :
			print("skipping document " + str(index))
			index += 1
			continue
		pickup_date = datetime.strptime(document["pickup_datetime"]["date"], "%Y-%m-%dT%H:%M:%S:%fZ")
		dropoff_date = datetime.strptime(document["dropoff_datetime"]["date"], "%Y-%m-%dT%H:%M:%S:%fZ")
		#cool = atetime.ISODate(cool)
		document["pickup_datetime"]["date"] = pickup_date
		document["dropoff_datetime"]["date"] = dropoff_date
		db.taxitest.update({"_id":document["_id"]}, document, True)
		index += 1
		#print(cool.day)
		#st = document["pickup_datetime"]["date"]
		#st = st[:-1]
		#cool = datetime.datetime.strptime( st, "%Y-%m-%dT%H:%M:%S:%f" )
		print("updating document: " + str(index))
	#for document in cursor:
	#	print(document)

	for document in cursor:
		print(document)

def indexInit():
	return 0

def processResults(flags):
	return 0


#buildIndexes()
#printAllDocs()
