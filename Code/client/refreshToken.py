import pyrebase
import os
import json
from time import sleep

# set the path to firebase config file to an environment variable
configFile = open(os.environ['FIREBASE_CONFIG'])
firebase = pyrebase.initialize_app(json.load(configFile))
auth = firebase.auth

def writeCurrUserInfo(jsonUserInfo):
    # path = /.creds/.currUser
    with open(os.environ['CURR_USER'], "w+") as file:
        file.write(json.dumps(jsonUserInfo))
        file.close()

def refreshToken():
    user = open(os.environ['CURR_USER'], "r")
    jsonUser = json.loads(user.read())
        
    # A user's idToken expires after 1 hour, so be sure to use the user's refreshToken to avoid stale tokens.
    jsonUser = auth.refresh(jsonUser['refreshToken'])
    writeCurrUserInfo(jsonUser)
    
if __name__ == '__main__':
    while(True):
        sleep(1800)
        refreshToken()
        
        statusFile = open(os.environ['CURR_STATUS'], "r")
        jsonStatusFile = json.loads(statusFile.read())
        if(jsonStatusFile['status'] == 'INACTIVE'):
            break
    