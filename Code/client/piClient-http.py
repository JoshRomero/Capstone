from time import sleep
from picamera import PiCamera
from datetime import datetime
from io import BytesIO
import ssl
import requests

# NEED TO: RESOLVE UNICODE ISSUE WITH IMAGE BYTES -- CURRENTLY CANNOT SEND IMAGES IN IN ENTRY FOR SOME REASON
# CHECK PI FOR NEWEST CODE

ROOM_ID = 1
items = {"keysProb": 0.0, "glassesProb": 0.0, "thermosProb": 0.0}

def createEntry(uid, captureTime, imageData):
    dbEntry = {"userID": uid,
               "dateTime": captureTime.strftime('%m-%d-%Y %I:%M:%S %p'),
               "roomID": ROOM_ID, 
               "keysProb": items["keysProb"],
               "glassesProb": items["glassesProb"],
               "thermosProb": items["thermosProb"],
               "image": imageData
    }
    
    return dbEntry

if __name__ == "__main__":
    # retrieve token for user
    
    # ssl handshake

    with PiCamera() as camera:
        #for upside down cameras (ribbon up)
        camera.rotation = 180
        camera.resolution = (1920, 1080)

        # create in-stream memory for image data
        imageMemoryStream = BytesIO()

        while True:
            # camera warm-up time
            sleep(.5)
            
            for item in items:
                items[item] = 0.0
            
            # capture image and append to in-memory byte stream
            captureTime = datetime.now()
            camera.capture(imageMemoryStream, 'jpeg')
            print("[+] Picture captured at the dateTime: {}".format(captureTime))
                
            # create database entry
            uid = "testID" # temporary, needs to be replaced by token
            items["keysProb"] = 1.0
            entry = createEntry(uid, captureTime, imageMemoryStream.getvalue())
            
            # clear in-memory byte stream
            imageMemoryStream.seek(0)
            imageMemoryStream.truncate(0)
            
            # send post request to server to insert image and related data
            for item in items:
                if items[item] == 1.0:   
                    url = "http://127.0.0.1:5000/{}/pidata/{}".format(uid, item)
                    requests.post(url, json=entry)
            
            # sleep a minute to give the database time to receive the last entry
            sleep(10)

