import pymongo
import ast

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
	#

	#cursor = db.taxitest.find()
#
	#for document in cursor :
#
	#	pickup_coord = document["pickup_loc"]
	#	dropoff_coord = document["dropoff_loc"]
#
	#	dropoff = {
	#		'loc' : dropoff_coord
	#	}
#
	#	pickup = {
	#		'loc' : pickup_coord
	#	}
#
	#	document.update({"pickup_loc" : pickup})
	#	document.update({"dropoff_loc" : dropoff})
	#	print(document)
	#	db.taxitest.update({"_id":document["_id"]}, document, True)

#
	#zzz = db.taxitest.find()
	#for document in zzz :
	#	print(document)

	#db.taxitest.create_index([("pickup_loc", pymongo.GEO2D)])
	#db.taxitest.create_index([("dropoff_loc", pymongo.GEO2D)])


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
	cursor = db.taxitest.find({"pickup_loc" : { "loc" : {"$near": [-73.980072, 40.743137]}}}).limit(3)
#

	#print("hello")
	for document in cursor :
		print(document)
		#db.taxitest.
#
	#return 1

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


	zzz = db.taxitest.find()
	for document in zzz :
		print(document)

def processResults(flags):
	return 0


mongoQuery(0)
