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
items = {"keysProb": 0.0, "glassesProb": 0.0, "thermosProb": 0.0}

def createEntry(uid, captureTime, imageData):
    dbEntry = {"userID": uid,
               "dateTime": captureTime,
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
            
            tmpImage = tempfile.NamedTemporaryFile(suffix = ".jpeg")
            tmpImageDir = tempfile.gettempdir() + "/" + tmpImage.name()
            
            # capture image and append to in-memory byte stream
            captureTime = datetime.now()
            camera.capture(tmpImageDir)
            print("[+] Picture captured at the dateTime: {}".format(captureTime))
                
            # create database entry
            uid = "testID" # temporary, needs to be replaced by token
            items["keysProb"] = 1.0  # temporary, needs to be replaced with tensorflow data
            entry = createEntry(uid, captureTime, open(tmpImageDir, "rb"))
            
            # send post request to server to insert image and related data
            for item in items:
                if items[item] == 1.0:   
                    url = "http://192.168.1.54:5000/{}/pidata/{}".format(uid, item[0:len(item) - 4])
                    requests.post(url, json=entry)
            
            # reset probability values for each item
            for item in items:
                items[item] = 0.0
                
            # sleep a minute to give the database time to receive the last entry
            sleep(10)

