

def mongoQuery(queryRequest):
	# we need dates and log/ lat of pick-up drop-off
	# maybe passenger count?
	#
	argsString = ""
	firstFlag = True;

	for key in queryRequest:
		print(key)
		if(firstFlag):
			argsString =  key + ":" + queryRequest[key]
		else:
			argString += argString + "," + key + ":" + queryRequest[key]
	return argsString;
