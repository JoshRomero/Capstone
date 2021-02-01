## Clark Foster
# This file sends a file over python socket using TCP

import socket
import os
from time import sleep
from picamera import PiCamera
from pymongo import MongoClient
from base64 import b64encode
from datetime import datetime

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # each step we will send 4096 bytes

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
    
    with open('../imgs/{}.jpeg'.format(saveDate), mode='rb') as image: # b is important -> binary
        imageContent = image.read()
    
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
    
    


