# This script count the number of times each object has been queried by the user

'''

THIS BLOCK OF CODE WAS WHEN WE WERE CONNECTING TO DB FROM DASHBOARD CODE

from pymongo import MongoClient
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
'''


import matplotlib.pyplot as plt

def dashboard(collection):
    ######## START GET DATA FOR OBJECT QUERIES BY TYPE ############################################################
    # initialize all counts to 0
    backPackQueries = 0
    suitcaseQueries = 0
    laptopQueries = 0
    cellPhoneQueries = 0
    umbrellaQueries = 0
    
    # search for and count all backpack queries
    curObject = "backpack"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      backPackQueries += 1
    
    # search for and count all suitcase queries
    curObject = "suitcase"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      suitcaseQueries += 1
    
    # search for and count all laptop queries
    curObject = "laptop"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      laptopQueries += 1
    
    # search for and count all cellphone queries
    curObject = "cellphone"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      cellPhoneQueries += 1
    
    # search for and count all umrella queries
    curObject = "umbrella"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      umbrellaQueries += 1
    ######## END GET DATA FOR OBJECT QUERIES BY TYPE ############################################################
    
    
    ######## START GET DATA FOR OBJECT QUERIES BY TIME OF DAY ############################################################
    mornQueries = 0
    aftrQueries = 0
    evenQueries = 0
    
    listQueries = collection.find({"morningQuery": 1}, {"queryDateTime": 1})
    for x in mornQueries:
      mornQueries += 1
    
    listQueries = collection.find({"afterQuery": 1}, {"queryDateTime": 1})
    for x in aftrQueries:
      aftrQueries += 1
    
    listQueries = collection.find({"evenQuery": 1}, {"queryDateTime": 1})
    for x in mornQueries:
      evenQueries += 1
    ######## END GET DATA FOR OBJECT QUERIES BY TIME OF DAY ############################################################
    
    
    # plot results in matplotlib
    
    # first subplot is how many queries by item type
    plt.title("Your Dashboard")
    plt.subplot(2,1,1)
    objNames = ["backpack", "suitcase", "laptop", "cellphone", "umbrella"]
    numQueries = [backPackQueries, suitcaseQueries, laptopQueries, cellPhoneQueries, umbrellaQueries]
    plt.bar(objNames, numQueries)
    
    # second subplot is a lines plot how many queries by time of day
    plt.subplot(2,1,2)
    queryTimes = ["morning", "afternoon", "evening"]
    numQueries = [mornQueries, aftrQueries, evenQueries]
    plt.plot(queryTimes, numQueries)
    
    
    # show plot
    plt.show()
    
    # save figure
    plt.savefig("dashboard.jpg")
