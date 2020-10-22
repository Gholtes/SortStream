import uuid
import pickle
from hashlib import sha256
import os
import requests
import json
import urllib.parse

def AuthenticateLicence(appPath = ".", licenceFilename = "sortstream.licence", X = 0):
	'''
	Grant Holtes 26/6/20
	Check if a licence file is valid for the machine it is running on
	'''
	#1) Open Licence, extract Z
	try:
		licenceData = pickle.load(open(os.path.join(appPath, licenceFilename), "rb" ))
		Zlic = licenceData["Z"]

		#2) Make Z from UUID, X
		UUID = uuid.getnode()
		Znew = getHash(UUID, X)

		#3) authenticate and take action
		if Zlic == Znew:
			return True
		else:
			#display a "no licence" error, ask for product key
			return False
	except FileNotFoundError:
		return False

def getHash(UUID = 0, X = 0):
	Product = UUID * X
	ByteProd = str.encode(str(Product))
	Z = sha256(ByteProd).hexdigest()
	return Z

def checkProductKey(productKey = 0):
	#0) apply some basic sense checks, protect API from injecton

	#check Type
	try:
		productKeyInt = int(productKey)
	except ValueError:
		returnMessage = "Please enter a 12 digit numeric product key without spaces"
		return False, returnMessage
	
	if len(str(productKey)) != 12:
		returnMessage = "Please enter a 12 digit numeric product key without spaces"
		return False, returnMessage

	#1) Call API with product key, UUID
	UUID = uuid.getnode()
	DynamoDBCall = readDynamoDBAPI(productKey)

	DB_UUID = DynamoDBCall["UUID"]
	DB_email = DynamoDBCall["email"]

	#2) Use response to either return Valid if this is a new key or has been used previously with this UUID
	validProductKey = False
	if int(DB_UUID) == -1: #This is the case where the product code has not yet been used, so is valid
		validProductKey = True
		#write the users UUID to this product code
		UpdateDynamoDBAPI(productKey, UUID = UUID) 
		returnMessage = "Product Key accepted, licence file created. Please restart application"
	elif int(UUID) == int(DB_UUID): #This is the case where the product code has been used but on this same computer, so is valid
		validProductKey = True
		#no update to DB required
		returnMessage = "Product Key accepted, licence file created. Please restart application"
	else:
		returnMessage = "This Product Key has already been used"

	return validProductKey, returnMessage

def writeLicenceFile(licenceFilename = "sortstream.licence", X = 0, productKey = 0, appPath = "."):
	'''Grant Holtes
	Generate a licence file with format:
	{
		Z: The hash of UUID, X
		Key: The product key used to generate the licence
	}
	'''
	UUID = uuid.getnode()
	Z = getHash(UUID, X)
	#make licence dict
	licence = {}
	licence["Z"] = Z
	licence["Key"] = productKey
	#write File
	with open(os.path.join(appPath, licenceFilename), "wb") as pickleFile: 
		pickle.dump(licence, pickleFile)
	
def readDynamoDBAPI(ProductKey, apiEndPoint = "https://r9uxgotjjc.execute-api.eu-west-1.amazonaws.com/default/lambda-microservice"):
	'''accepts a productKey, apiEndPoint
	returns all info about the unique row in the DB for the given product code in a dict.
	keys: "productkey", "email", "uuid_"
	if productKey doesnt exist in the DB, returns {ProductKey: productkey, email: None, UUID: None}
	'''

	Params = {
	"operation": "read",
	"tableName": "DocumentClassificationLicence",
	"payload": { 
		"Key": 
			{ "productkey": str(ProductKey)
			}
		}
	}
	#send get request
	getReq = requests.get(url = apiEndPoint, json = Params) 
	response = getReq.json() 
	try:
		productInfo = response["Item"]
		returnDict = {}
		returnDict["productkey"] = productInfo["productkey"]
		returnDict["email"] = productInfo["email"]
		returnDict["UUID"] = productInfo["uuid_"]
	except KeyError:
		returnDict = {}
		returnDict["productkey"] = ProductKey
		returnDict["email"] = None
		returnDict["UUID"] = None
	return returnDict

def UpdateDynamoDBAPI(ProductKey, UUID = -1, apiEndPoint = "https://r9uxgotjjc.execute-api.eu-west-1.amazonaws.com/default/lambda-microservice"):
	'''accepts a productKey, UUID, apiEndPoint
	Updates the unique row in the DB with a new uuid_ value as given by the UUID input.
	returns a success status (True = successful update, False = failed update)
	'''

	#1) Send update request 

	Params = {
  		"operation": "update",
  		"tableName": "DocumentClassificationLicence",
  		"payload": {
    	"Key": {
      		"productkey": str(ProductKey)
    	},
    	"UpdateExpression": "set uuid_ = :u",
    	"ExpressionAttributeValues": {
      		":u": str(UUID)
    		},
    	"ReturnValues": "UPDATED_NEW"
  		}
	}

	#send get request with payload
	getReq = requests.get(url = apiEndPoint, json = Params) 
	try:
		response = getReq.json()
		newUUID = response['Attributes']['uuid_']
		if int(UUID) == int(newUUID):
			return True
		else:
			return False
	except:
		print("error in updating dynomoDB request")
		return False

def createDynamoDBAPI(ProductKey, email, UUID = -1, apiEndPoint = "https://r9uxgotjjc.execute-api.eu-west-1.amazonaws.com/default/lambda-microservice"):
	'''accepts a productKey, email, uuid, apiEndPoint
	Creates a new item in the DB with the productKey, email, uuid provided. useful for enrolling new product keys.
	returns True if successful.
	'''

	Params = {
  		"operation": "create",
  		"tableName": "DocumentClassificationLicence",
  		"payload": {
    		"Item": {
    			"productkey": str(ProductKey),
      			"email": email,
      			"uuid_": str(UUID)
    		}
  		}
	}

	#send get request
	try:
		requests.get(url = apiEndPoint, json = Params) 
		return True
	except:
		return False

