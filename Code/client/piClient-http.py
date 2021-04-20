from time import sleep
from picamera import PiCamera
from datetime import datetime
from io import BytesIO
import ssl
import requests
import tempfile
from base64 import b64encode
import json
import pyrebase

email = "johndoe@gmail.com"
password = "Pa55w0rd!"

config = {
  "apiKey": "AIzaSyDkYMP_ilWmPr5n0Kt_N7odVehYEw6qh64",
  "authDomain": "objectfinder-3d3f3.firebaseapp.com",
  "databaseURL": "https://objectfinder-3d3f3-default-rtdb.firebaseio.com",
  "storageBucket": "objectfinder-3d3f3.appspot.com"
}
firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)
header = {"Authorization": user["idToken"]}

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
            #uid = "qNZFhdvgnIgdSnORNpmbgqlFO7S2" # temporary, needs to be replaced by token
            items["keysProb"] = 1.0  # temporary, needs to be replaced with tensorflow data
            imageData = tmpImage.read()
            entry = createEntry(user["localId"], captureTime)

            file = {"image": open(tmpImage.name, 'rb')}
            
            # send post request to server to insert image and related data
            url = "https://objectfinder.tech/pidata"
            r = requests.post(url, files=file, data=entry, headers=header)
            print(r)
            
            # reset probability values for each item
            for item in items:
                items[item] = 0.0
                
            # sleep a minute to give the database time to receive the last entry
            sleep(10)