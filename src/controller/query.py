import pymongo
from bson.json_util import dumps
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
	dt["ud"] = d + timedelta(days=1)
	dt["ld"] = d + timedelta(days= -1)
	return dt

def polygonQuery(queryRequest, pickupDropoff):
	print(queryRequest["bounds"])
	print(type(queryRequest["bounds"]))
	d = queryRequest["p_dt"]
	d = datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))
	ud = d + timedelta(hours=6)
	ld = d + timedelta(hours= -6)

	#"pickup_datetime.date":d is the pickup query param
	# cursor = db.taxitest.find({ 'pickup_loc.loc' : { '$geoNear' : [-73.980072, 40.743137]}}).limit(5)
	print("Launching find")
	if(pickupDropoff):
		cursor = db.taxitest.find({"pickup_datetime.date":{"$gt":ld,"$lt":ud},
		"pickup_loc.loc":{"$geoWithin": {"$polygon": queryRequest["bounds"]}}
		},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)
	else:
		cursor = db.taxitest.find({"dropoff_datetime.date":{"$gt":ld,"$lt":ud},
		"dropoff_loc.loc":{"$geoWithin": {"$polygon": queryRequest["bounds"]}}
		},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)
	print("Dumping Cursor")
	print(cursor.explain())
	return dumps(cursor)


# Circle queryRequest "bounds" should be in format [[<x>, <y>], <radius>]
def circleQuery(queryRequest, pickupDropoff):
	print(queryRequest["bounds"])
	print(type(queryRequest["bounds"]))
	d = queryRequest["p_dt"]
	d = datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))
	ud = d + timedelta(hours=6)
	ld = d + timedelta(hours= -6)
	cursor = db.taxitest.find().limit(5)
	for document in cursor:
		print(document)
	#"pickup_datetime.date":d is the pickup query param
	# cursor = db.taxitest.find({ 'pickup_loc.loc' : { '$geoNear' : [-73.980072, 40.743137]}}).limit(5)
	print("Launching find")
	# true is a pickup query, false is dropoff query
	if(pickupDropoff):
		cursor = db.taxitest.find({"pickup_datetime.date":{"$gt":ld,"$lt":ud},
		"pickup_loc.loc":{"$geoWithin": {"$centerSphere": queryRequest["bounds"]}}
		},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)
	else:
		cursor = db.taxitest.find({"dropoff_datetime.date":{"$gt":ld,"$lt":ud},
		"dropoff_loc.loc":{"$geoWithin": {"$center": queryRequest["bounds"]}}
		},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)

	print("Dumping Cursor")
	print(cursor.explain())
	return dumps(cursor)


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
