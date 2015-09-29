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

	db.taxitest.update_many({'pickup_longitude': *, 'pickup_latitude': *},)
	#argsString = ""
	#firstFlag = True;

	#for key in queryRequest:
		#print(key)
	#	pickup_longitude": -73.980072,
	#					    "pickup_latitude": 40.743137,
		#if(firstFlag):
			#argsString = "{'$geometry':{'" + key + "':{'$near' :[" + queryRequest[key] + "]}"
			#firstFlag = False;		
	#argsString = "{'location':{'$near':{'$geometry':{'type':'Point', 'coordinates' : [-73.980072, 40.743137]},"
	#argsString += "'$maxDistance':100000, '$minDistance':0}}}"
	
	#print(argsString)
	#qString = ast.literal_eval(argsString)
	#cursor = db.taxitest.find(qString)

	#for document in cursor :
	#	print(document)

	return 1

def processResults(flags):
	return 0
