import pymongo

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
	firstFlag = True;

	for key in queryRequest:
		print(key)
		if(firstFlag):
			argString =  key + ":" + queryRequest[key]
			firstFlag = False;
		else:
			argString += "," + key + ":" + queryRequest[key]
	print(argString);
	cursor = db.taxitest.find()
	return cursor

def processResults(flags):
	return 0
