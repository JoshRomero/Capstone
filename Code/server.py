from pymongo import MongoClient
from base64 import b64decode
from PIL import Image
from io import BytesIO
from socket import *

# host machine ip, mongodb and server listening port
DATABASE_DOMAIN = SERVER_DOMAIN = "192.168.1.54"
DATABASE_PORT = 27017
SERVER_PORT = 12001


def queryDatabase(object):
    # retrieve the newest document from the collection based on datetime (will be changed later to include CNN results)
    for entry in camNodeResultsCollection.find().sort("dateTime", -1):
        newestEntry = entry
        break
    
    # retrieve the image data and date time
    encryptedImageData = newestEntry["image"]
    dateAndTime = newestEntry["dateTime"]

    # unencrypt b64 encrypted image data
    unencryptedImageData = b64decode(encryptedImageData)

    # CAN BE USED IN THE GUI
    # # create in-stream memory for image data
    # imageMemoryStream = BytesIO(unencryptedImageData)
    # # temporarily display queried image
    # image = Image.open(BytesIO(unencryptedImageData))
    # image.show()
    # # clear in-memory byte stream
    # imageMemoryStream.seek(0)
    # imageMemoryStream.truncate(0)

    # CURRENT TEMPORARY WAY TO SAVE QUERIED IMAGES
    # save unencrypted image to a folder known as serverImgs
    with open('../serverImgs/{}.jpeg'.format(dateAndTime), mode='wb') as newImage:
        unencryptedImageData = bytearray(unencryptedImageData)
        newImage.write(unencryptedImageData)
        print("[+] Entry image saved in serverImgs folder with name: {}.jpeg".format(dateAndTime))
        newImage.close()

def establishDatabaseConnection():
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
    
# def setupServer():
    
#     # create TCP server socket and bind to PORT
#     serverSocket = socket(AF_INET, SOCK_STREAM)
#     serverSocket.bind((SERVER_DOMAIN, SERVER_PORT))
    
#     # allow socket to listen for connections
#     serverSocket.listen()
#     print("Server is ready to receive connections!")
    
#     return serverSocket
    
    
# MAIN

# establishDatabaseConnection()

# create TCP server socket and bind to PORT
serverSocket = create_server((SERVER_DOMAIN, SERVER_PORT))
print("Server is ready to receive connections!")

while True:
    # create connection socket and receive request message from connection socket
    connectionSocket, address = serverSocket.accept()
    print("Connection from {} accepted!".format(address))

    
# for testing purposes only
# queryDatabase("phone")