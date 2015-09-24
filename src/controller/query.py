def mongoQuery(queryRequest):
	queryToExecute = deconstructQuery(httpRequest)
	# we need dates and log/ lat of pick-up drop-off
	# maybe passenger count? 
	# 
	argsString = ""
	i = 0
	for key, in queryRequest:
		if (i != 0) 
			argsString =  key + ":" + queryRequest[key]
			++i
		else
			argString += argString + "," + key + ":" + queryRequest[key]

	print argString	
	return 0