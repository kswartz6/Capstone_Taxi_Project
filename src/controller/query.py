import pymongo
from bson.json_util import dumps
import ujson
from datetime import datetime, timedelta

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

#	below is sample query for a given location
# 	cursor = db.taxitest.find({"pickup_loc" : { "loc" : {"$near": [-73.980072, 40.743137]}}}).limit(3)


#bulkQuery grabs 100 records
def bulkQuery():
	cursor = db.taxitest.find().limit(100)
	return cursor

def fixData(data):
	cursor = db.taxitest.find()

	for document in cursor :
		document["pickup_loc"] = [document["pickup_longitude"], document["pickup_latitude"]]
		document["dropoff_loc"] = [document["dropoff_longitude"], document["dropoff_latitude"]]
		document.pop("pickup_longitude")
		document.pop("pickup_latitude")
		document.pop("dropoff_longitude")
		document.pop("dropoff_latitude")
		db.taxitest.update({"_id":document["_id"]}, document, True)


	test = db.taxitest.find()
	for document in test:
		print(document)


def indexInit():
	return 0

def processResults(flags):
	return 0
