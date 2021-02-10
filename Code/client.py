from time import sleep
from picamera import PiCamera
from pymongo import MongoClient
from base64 import b64encode
from datetime import datetime
from io import BytesIO

# host machine ip and mongodb port
DATABASE_DOMAIN = '192.168.1.54'
DATABASE_PORT = 27017

ROOM_ID = 1
KEYS_PROB = 0.0
PHONE_PROB = 0.0
THERMOS_PROB = 0.0
WALLET_PROB = 0.0

def createEntry(imageData):
    dbEntry = {"dateTime": datetime.now(),
               "roomID": ROOM_ID,
               "keysProb": KEYS_PROB,
               "phoneProb": PHONE_PROB,
               "thermosProb": THERMOS_PROB,
               "walletProb": WALLET_PROB,
               "image": b64encode(imageData)
    }
    
    return dbEntry

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
    print("[+] Successfully Authenticated")
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

with PiCamera() as camera:
    #for upside down cameras (ribbon up)
    camera.rotation = 180
    camera.resolution = (1920, 1080)

    # create in-stream memory for image data
    imageMemoryStream = BytesIO()

    while True:
        # camera warm-up time
        sleep(.5)
        
        # capture image and append to in-memory byte stream
        captureTime = datetime.now()
        camera.capture(imageMemoryStream, 'jpeg')
        print("[+] Picture captured at the dateTime: {}".format(captureTime))
            
        # create database entry
        entry = createEntry(imageMemoryStream.getValue())
        
        # clear in-memory byte stream
        imageMemoryStream.seek(0)
        imageMemoryStream.truncate(0)
            
        # insert created database entry
        camNodeResultsCollection.insert_one(entry)
        print("[+] Entry made for picture @ {}".format(captureTime))
        
        # sleep a minute to give the database time to receive the last entry
        sleep(55.5)

