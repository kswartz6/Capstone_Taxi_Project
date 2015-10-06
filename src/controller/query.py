import pymongo
import ast
from bson.son import SON

MONGO_DB_URI = "mongodb://bob:bob@ds051368.mongolab.com:51368/csf2015capstone"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.csf2015capstone


#mongoQuery is a universal deconstructor - we grab ALL params from
#queryRequest obj and then we concatenate to create the query string

#returns cursor object for now. We do processing of documents in cursor within other
#functions?
def mongoQuery(queryRequest):
	# we need dates and log/ lat of pick-up drop-off
	# maybe passenger count?
	argString = ""
	firstFlag = True
	for key in queryRequest:
		print(key)
		if(firstFlag):
			argString =  key + ":" + queryRequest[key]
			firstFlag = False;
		else:
			argString += "," + key + ":" + queryRequest[key]
	print(argString)
	cursor = db.taxitest.find()
	return cursor

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
	if(pickup_date == None):
		#do nothing
		continue
	else:
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
	if(dropoff_date == None):
		#do nothing
		continue
	else:
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
		print("currently updating: " + current_doc_number)
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
		print("done updating: " + current_doc_number)
		current_doc_number = current_doc_number + 1

	print("Currently creating geospatial indexing on pickup_loc")
	db.taxitest.create_index({"pickup_loc.loc", pymongo.GEO2D})
	
	print("Currently creating geospatial indexing on dropoff_loc")
	db.taxitest.create_index({"dropoff_loc.loc", pymongo.GEO2D})


def printAllDocs():
	cursor = db.taxitest.find()

	for document in cursor:
		print(document)

def processResults(flags):
	return 0

printAllDocs()