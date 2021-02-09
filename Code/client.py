from time import sleep
from picamera import PiCamera
from pymongo import MongoClient
from base64 import b64encode
from datetime import datetime
import tempfile

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
    
#camera setup
camera = PiCamera()
#only for my set up, camera was upside down (ribbon up)
camera.rotation = 180
camera.resolution = (1920, 1080)

while True:
    # camera needs to get ready
    sleep(.5)
    
    # take the picture and saves as temp file to be deleted upon closing
    saveDate = datetime.now()
    with tempfile.TemporaryFile(mode='wb') as tmp:
        camera.capture(tmp)
        
        # create database entry
        entry = createEntry(imageContent)
        
        # insert created database entry
        camNodeResultsCollection.insert_one(entry)
        print("[+] Entry made for picture @ {}".format(saveDate))

        tmp.close()
    
    # sleep a minute to give the database time to receive the last entry
    sleep(55.5)

