from collections import deque
from helpers import *

# DO NOT REMOVE THESE COMMENTS
# http://www.jsonschema.net/#
# Above URL is used to create schema from response

schemaDirPath = getWorkingDirectory() + "/schema/"
resultDirPath = getWorkingDirectory() + "/result/"
todayDate = getTodayDate()
numResponseValidated = 0
numResponseInvalid = 0
tempUrl = ""
errMsg = ''

f = open("../mapping.json", "r")
json_obj = json.loads(f.read())
f.close()

print("Starting API responses validation")

for i in json_obj['mapping']:
	response = getUrlResponse(i['url'])
	
	f = open(schemaDirPath + i["schema_file_name"], "r")
	schema = f.read();
	f.close()
	
	try:
		v = jsonschema.Draft3Validator(json.loads(schema))
		if v.is_valid(response) != True:
			errMsg = '============================================================\n'
			errMsg += "url: " + i['url'] + "\n"
			errMsg += "schema file: " + i['schema_file_name'] + "\n"
			errMsg += "--------------------- Errors -----------------------------\n"
			numResponseInvalid = numResponseInvalid + 1
			tempUrl = tempUrl + i['url'] + " => FAIL \n"
		else:
			numResponseValidated = numResponseValidated + 1
			tempUrl = tempUrl + i['url'] + " => PASS \n"
			
		for error in sorted(v.iter_errors(response), key=str):
			path = ''
			while error.path:
				path += "/" + str(error.path.popleft())
			errMsg += path + "\n"
			errMsg += error.message + "\n"
			errMsg += "\n"
			log(errMsg, resultDirPath + "/" + "error.txt")
			
	except jsonschema.ValidationError as e:
		log(e.message, resultDirPath + "/" + "errlog.txt")

msg = tempUrl
msg += '\nTotal responses validated: ' + str(numResponseInvalid + numResponseValidated) + '\n'
msg += 'Total valid response: ' + str(numResponseValidated) + '\n'
msg += 'Total invalid response: ' + str(numResponseInvalid) + '\n'
log(msg + errMsg, resultDirPath + "/" + "success.txt")

print("End response validation")