from time import sleep
from picamera import PiCamera
from datetime import datetime
from io import BytesIO
import ssl
import requests
import tempfile

# NEED TO: RESOLVE UNICODE ISSUE WITH IMAGE BYTES -- CURRENTLY CANNOT SEND IMAGES IN IN ENTRY FOR SOME REASON
# CHECK PI FOR NEWEST CODE

ROOM_ID = 1
items = {"keysProb": 0.0, "glassesProb": 0.0, "remoteProb": 0.0}

def createEntry(uid, captureTime):
    dbEntry = {"userID": uid,
               "dateTime": captureTime,
               "roomID": ROOM_ID, 
               "keysProb": items["keysProb"],
               "glassesProb": items["glassesProb"],
               "remoteProb": items["remoteProb"],
    }
    
    return dbEntry

if __name__ == "__main__":
    # retrieve token for user

    with PiCamera() as camera:
        #for upside down cameras (ribbon up)
        camera.rotation = 180
        camera.resolution = (1920, 1080)

        while True:
            # camera warm-up time
            sleep(.5)
            
            tmpImage = tempfile.NamedTemporaryFile(suffix = ".jpeg")
            print(tmpImage.name)
            
            # capture image and append to in-memory byte stream
            captureTime = datetime.now()
            camera.capture(tmpImage.name)
            print("[+] Picture captured at the dateTime: {}".format(captureTime))
                
            # create database entry
            uid = "testID" # temporary, needs to be replaced by token
            items["keysProb"] = 1.0  # temporary, needs to be replaced with tensorflow data
            imageData = tmpImage.read()
            
            file = {"image": open(tmpImage.name, 'rb')}
            entry = createEntry(uid, captureTime)
            
            # send post request to server to insert image and related data
            url = "http://18.188.84.183:12001/pidata"
            r = requests.post(url, files=file, data=entry)
            
            # reset probability values for each item
            for item in items:
                items[item] = 0.0
                
            # sleep a minute to give the database time to receive the last entry
            sleep(10)

