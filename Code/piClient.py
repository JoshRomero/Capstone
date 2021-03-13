from time import sleep
from picamera import PiCamera
from pymongo import MongoClient
from datetime import datetime
from io import BytesIO
import struct
import json
from socket import *

# pi server ip and port
SERVER_DOMAIN = "18.191.21.213"
SERVER_PORT = 24002

ROOM_ID = 1
KEYS_PROB = 0.0
PHONE_PROB = 0.0
THERMOS_PROB = 0.0
WALLET_PROB = 0.0

def createEntry(uid, savedDateTime):
    dbEntry = {"userID": uid,
               "dateTime": savedDateTime,
               "roomID": ROOM_ID,
               "keysProb": KEYS_PROB,
               "phoneProb": PHONE_PROB,
               "thermosProb": THERMOS_PROB,
               "walletProb": WALLET_PROB,
               "image": ""
    }
    
    return dbEntry

def sendMessage(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

if __name__ == "__main__":
    # retrieve token for user
    
    # connect to server socket
    clientSocket = create_connection((SERVER_DOMAIN, SERVER_PORT))    

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
            camera.capture(imageMemoryStream, 'jpg')
            print("[+] Picture captured at the dateTime: {}".format(captureTime))
            
            imageBytes = bytearray()
            for byte in imageMemoryStream:
                imageBytes.append(byte)
            
            # clear in-memory byte stream
            imageMemoryStream.seek(0)
            imageMemoryStream.truncate(0)
                
            # create database entry
            entry = createEntry(imageMemoryStream.getvalue(), captureTime)
            
            # using encode() + dumps() to convert to bytes 
            entryBytes = json.dumps(entry).encode('utf-8')
                
            # send entry and image to server
            sendMessage(clientSocket, entryBytes)
            sendMessage(clientSocket, imageBytes)
            
            # sleep a minute to give the database time to receive the last entry
            sleep(55.5)

