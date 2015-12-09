import pymongo
from bson.json_util import dumps
import ast
from bson.son import SON
from datetime import *

MONGO_DB_URI = "mongodb://localhost:27017/csf2015capstone"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.csf2015capstone
#returns cursor object for now. We do processing of documents in cursor within other
#functions?
#queryRequest should ALWAYS contain p_dt and bounds
#pdt = pickup date time
#bounds = coord points of polygon on leaflet
#bounds MUST be an iterable of iterables such that [ [x1, y1], [x2, y2] ]

def buildDateTime(dateTimeArray):
	return datetime(int(dateTimeArray[0]),int(dateTimeArray[1]),int(dateTimeArray[2]),int(dateTimeArray[3]),int(dateTimeArray[4]),int(dateTimeArray[5]))

def setDateBounds(date, hours):
	mins = hours * 60;
	return date + timedelta(minutes=mins)

def polygonQuery(queryRequest, pickupDropoff):
	d = buildDateTime(queryRequest["p_dt"])

	ud = setDateBounds(d, 6)
	ld = setDateBounds(d, -6)

	print("Launching find")
	if(pickupDropoff):
		cursor = db.taxitest.find({"pickup_datetime.date":{"$gt":ld,"$lt":ud},
		"pickup_loc.loc":{"$geoWithin": {"$polygon": queryRequest["bounds"]}}
		}, batch_size=2000)
	else:
		cursor = db.taxitest.find({"dropoff_datetime.date":{"$gt":ld,"$lt":ud},
		"dropoff_loc.loc":{"$geoWithin": {"$polygon": queryRequest["bounds"]}}
		}, batch_size=2000)

	print("Dumping Cursor")
	print(cursor.explain())
	return dumps(cursor)

# Circle queryRequest "bounds" should be in format [[<x>, <y>], <radius>]
def circleQuery(queryRequest, pickupDropoff):
	d = buildDateTime(queryRequest["p_dt"])

	ud = setDateBounds(d, 6)
	ld = setDateBounds(d, -6)
	
	print("Launching find")
	# true is a pickup query, false is dropoff query
	if(pickupDropoff):
		cursor = db.taxitest.find({"pickup_datetime.date":{"$gt":ld,"$lt":ud},
		"pickup_loc.loc":{"$geoWithin": {"$centerSphere": queryRequest["bounds"]}}
		}, batch_size=2000)
	else:
		cursor = db.taxitest.find({"dropoff_datetime.date":{"$gt":ld,"$lt":ud},
		"dropoff_loc.loc":{"$geoWithin": {"$centerSphere": queryRequest["bounds"]}}
		}, batch_size=2000)

	print("Dumping Cursor")
	print(cursor.explain())
	return dumps(cursor)

def nearestPointQuery(queryRequest, pickupDropoff):
	d = queryRequest["p_dt"]
	d = datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))
	ud = d + timedelta(hours=6)
	ld = d + timedelta(hours= -6)
	
	coord = queryRequest["bounds"][0]
	radius = queryRequest["bounds"][1]

	print("Launching find")
	# true is a pickup query, false is dropoff query
	if(pickupDropoff):
		cursor = db.taxitest.find({"pickup_datetime.date":{"$gt":ld,"$lt":ud},
		"pickup_loc.loc" : { "$geoNear" : coord, "$maxDistance" : radius }
		},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)
	else:
		cursor = db.taxitest.find({"dropoff_datetime.date":{"$gt":ld,"$lt":ud},
		"dropoff_loc.loc":{"$geoWithin": {"$center": queryRequest["bounds"]}}
		},{"_id":0, "trip_distance":0,"vendor_id":0,"rate_code":0,"hack_license":0}, batch_size=2000)

	print("Dumping Cursor")
	print(cursor.explain())
	return dumps(cursor)
