from pymongo import MongoClient
from socket import *
from datetime import datetime

# host machine ip, mongodb and server listening port
DATABASE_DOMAIN = SERVER_DOMAIN = "192.168.1.54"
DATABASE_PORT = 27017
SERVER_PORT = 12001
SEPARATOR = "<SEPARATOR>"

def queryDatabase(object, collection):
    # retrieve the newest document from the collection based on datetime (will be changed later to include CNN results)
    for entry in collection.find().sort("dateTime", -1):
        newestEntry = entry
        break
    
    # extract and format necessary information
    necessaryInfo = str(newestEntry["dateTime"]) + SEPARATOR + str(newestEntry["roomID"]) + SEPARATOR + newestEntry["image"].decode('ascii')
    
    return necessaryInfo

# connect to the database
try:
    print("Connecting to mongoDB server @ {}:{}...".format(DATABASE_DOMAIN, DATABASE_PORT))
    mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    print("Connected!")
except:
    print("Connection failed")
    exit(0)

# authenticate to database
try:
    rPiDatabase = mongo_client.rPiData
    print("Authenticating to rPiData database...")
    rPiDatabase.authenticate(name='serverNode', password='7$dsV!G3D0Oc')
    print("Sucessfully Authenticated!")
except:
    print("Authentication failed")
    exit(0)

# switch to correct collection
try:
    print("Switching to camNodeResults collection...")
    camNodeResultsCollection = rPiDatabase.camNodeResults
    print("Successfully switched!")
except:
    print("Switch failed!")

# create TCP server socket and bind to PORT
serverSocket = create_server((SERVER_DOMAIN, SERVER_PORT))

# keep socket listening for a single connection
serverSocket.listen(1)
print("Server is ready to receive a connection...")

while True:
    # create connection socket
    connectionSocket, address = serverSocket.accept()
    print("Connection from {} accepted!".format(address))
    
    # receive request message from connection socket
    incomingRequest = connectionSocket.recv(1024).decode()
    while(len(incomingRequest) == 0):
        incomingRequest = connectionSocket.recv(1024).decode()
        
    print("Item requested from client: {} at {}".format(incomingRequest, datetime.now()))
    
    # query database and send requested information from query to sender
    requestedInformation = queryDatabase(incomingRequest, camNodeResultsCollection)
    connectionSocket.sendall(requestedInformation.encode())