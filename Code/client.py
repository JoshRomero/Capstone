## Clark Foster
# This file sends a file over python socket using TCP

from time import sleep
from picamera import PiCamera
from pymongo import MongoClient
from base64 import b64encode
from datetime import datetime

# host machine ip and mongodb port
DATABASE_DOMAIN = '192.168.1.54'
DATABASE_PORT = 27017

ROOM_ID = 1
KEYS_PROB = 0.0
PHONE_PROB = 0.0
THERMOS_PROB = 0.0
WALLET_PROB = 0.0

#camera setup
camera = PiCamera()
#only for my set up, camera was upside down
camera.rotation = 180
# i found the less resolution made it easier to send
camera.resolution = (1024, 768)

# connect to the server
try:
    print("[+] Connecting to mongoDB server @ {}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    print("[+] Connected")
except:
    print("[-] Connection failed")
    exit(0)

# authenticate to database
try:
    rPiDatabase = mongo_client.rPiData
    print("[+] Authenticating to rPiData database...")
    rPiDatabase.authenticate(name='rPiCamNode', password='G7q1D^3Bh3Ql')
    print("[+] Sucessfully Authenticated")
except:
    print("[-] Authentication failed")
    exit(0)

# switch to correct collection
try:
    print("[+] Switching to camNodeResults collection...")
    camNodeResultsCollection = rPiDatabase.camNodeResults
    print("[+] Successfully switched")
except:
    print("[-] Switch failed")

while True:
    # camera needs to get ready
    sleep(.5)
    
    # take the picture
    saveDate = datetime.now()
    camera.capture('../imgs/{}.jpeg'.format(saveDate))
    print("[+] Picture captured with the name: {}.jpeg".format(saveDate))
    
    # save captured image data to be converted into b64
    with open('../imgs/{}.jpeg'.format(saveDate), mode='rb') as image:
        imageContent = image.read()
        image.close()
    
    # create database entry
    dbEntry = {"dateTime": datetime.now(),
               "roomID": ROOM_ID,
               "keysProb": KEYS_PROB,
               "phoneProb": PHONE_PROB,
               "thermosProb": THERMOS_PROB,
               "walletProb": WALLET_PROB,
               "image": b64encode(imageContent)
    }
    
    # insert created database entry
    camNodeResultsCollection.insert_one(dbEntry)
    print("[+] Entry made for picture: {}.jpeg".format(saveDate))
    
    # sleep a minute to give the database time to receive the last entry
    sleep(60)

    # exit after the first image just for testing
    exit(0)

