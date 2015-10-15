import pymongo

MONGO_DB_URI = "mongodb://bob:bob@ds051368.mongolab.com:51368/csf2015capstone"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.csf2015capstone


#returns cursor object for now. We do processing of documents in cursor within other
#functions?
#queryRequest should ALWAYS contain p_dt and bounds
#pdt = pickup date time
#bounds = coord points of polygon on leaflet
#bounds MUST be an iterable of iterables such that [ [x1, y1], [x2, y2] ]
def mongoQuery(queryRequest):
	print(queryRequest["bounds"])
	#"pickup_datetime":queryRequest["p_dt"] is the pickup query param
	cursor = db.taxitest.find({
	"pickup_loc":{"loc":{"$geoWithin": {"$polygon": queryRequest["bounds"]}}}}).limit(100)
	print("!!!!1 FOUND STUFF")
	return cursor

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


def processResults(flags):
	return 0
