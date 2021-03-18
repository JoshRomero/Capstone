# This script count the number of times each object has been queried by the user

from pymongo import MongoClient
import matplotlib.pyplot as plt

# IP and port of EC2 instance
DATABASE_DOMAIN = "18.188.84.183"
DATABASE_PORT = 27017

# connect and authenticate and switch to correct collection
try:
    print("Connecting to mongoDB server @ {}:{}...".format(DATABASE_DOMAIN, DATABASE_PORT))
    mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    print("Connected!")
except:
    print("Connection failed")
    exit(0)
try:
    rPiDatabase = mongo_client.rPiData
    print("Authenticating to rPiData database...")
    rPiDatabase.authenticate(name='serverNode', password='7$dsV!G3D0Oc')
    print("Sucessfully Authenticated!")
except:
    print("Authentication failed")
    exit(0)
try:
    print("Switching to camNodeResults collection...")
    camNodeResultsCollection = rPiDatabase.camNodeResults
    print("Successfully switched!")
except:
    print("Switch failed!")

# initialize all counts to 0
backPackQueries = 0
suitcaseQueries = 0
laptopQueries = 0
cellPhoneQueries = 0
umbrellaQueries = 0
'''
# search for and count all backpack queries
curObject = "backpack"
#myquery = { "objectQueried": curObject}, { "objectQueried": 1 } 
listQueries = camNodeResultsCollection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )

for x in listQueries:
  backPackQueries += 1

# search for and count all suitcase queries
curObject = "suitcase"
myquery = { "objectQueried": curObject}, { "objectQueried": 1 } 
listQueries = camNodeResultsCollection.find(myquery)

for x in listQueries:
  suitcaseQueries += 1

# search for and count all laptop queries
curObject = "laptop"
myquery = { "objectQueried": curObject}, { "objectQueried": 1 } 
listQueries = camNodeResultsCollection.find(myquery)

for x in listQueries:
  laptopQueries += 1
'''
# search for and count all cellphone queries
curObject = "cellphone"
listQueries = camNodeResultsCollection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )

for x in listQueries:
  cellPhoneQueries += 1
'''
# search for and count all umrella queries
curObject = "umbrella"
myquery = { "objectQueried": curObject}, { "objectQueried": 1 } 
listQueries = camNodeResultsCollection.find(myquery)

for x in listQueries:
  umbrellaQueries += 1

'''
# plot results in matplotlib

objNames = ["backpack", "suitcase", "laptop", "cellphone", "umbrella"]
numQueries = [backPackQueries, suitcaseQueries, laptopQueries, cellPhoneQueries, umbrellaQueries]
plt.bar(objNames, numQueries)
plt.show()
'''
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
objNames = ["backpack", "suitcase", "laptop", "cellphone", "umbrella"]
numQueries = [backPackQueries, suitcaseQueries, laptopQueries, cellPhoneQueries, umbrellaQueries]
ax.bar(objNames, numQueries)
ax.set_title('Number of queries by object type')
plt.show()
'''