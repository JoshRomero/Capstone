# webserver imports
from flask import Flask, request
from flask_restful import abort, Api, Resource
from marshmallow import fields, Schema
import pyrebase
import json
import os
import requests

class UserLoginSchema(Schema):
    email = fields.Str()
    password = fields.Str()

class SystemRoomSchema(Schema):
    room = fields.Str()

class SystemStatusSchema(Schema):
    status = fields.Str()
    
app = Flask(__name__)
api = Api(app)

# set the path to firebase config file to an environment variable
configFile = open(os.environ['FIREBASE_CONFIG'])
firebase = pyrebase.initialize_app(json.load(configFile))

userLoginScheme = UserLoginSchema()
systemRoomScheme = SystemRoomSchema()
systemStatusScheme = SystemRoomSchema()

# refresh token every 30 mins in a seperate thread
def refreshToken():
    with open(os.environ['CURR_USER'], "r") as file:
        jsonUser = json.loads(file.read())
        file.close()
        
    # A user's idToken expires after 1 hour, so be sure to use the user's refreshToken to avoid stale tokens.
    jsonUser = auth.refresh(jsonUser['refreshToken'])
    writeCurrUserInfo(jsonUser)

def writeCurrUserInfo(jsonUserInfo):
    # path = /.creds/.currUser
    with open(os.environ['CURR_USER'], "w+") as file:
        file.write(jsonUserInfo)
        file.close()

# remove user info file
def deleteCurrUserInfo():
    os.remove(os.environ['CURR_USER'])

# send a post request to server containing the iPhone's idToken and the current Pi's idToken to compare uids 
def compareUUIDs(userIdToken):
    jsonUser = open(os.environ['CURR_USER'], "r")
    jsonUser = json.loads(json.read())
        
    header = {"Authorization": jsonUser["idtoken"]}
    payload = {"idToken": userIdToken}
    url = "https://objectfinder.tech/compareuuid"
    r = requests.post(url, json=payload, headers=header)
    rDict = json.loads(r.text)
        
    if rDict["equivalentUUIDS"] == "true":
        return True
    else:
        return False

# write user defined roomID to the roomID info file
def changeRoomID(newRoomID):
    systemRoomInfo = {"roomID": newRoomID}
    with open(os.environ['ROOM_ID'], 'w') as file:
        file.write(systemRoomInfo)
        file.close()

# user sends credentials to pi -> pi logs in once -> pi saves the token to the file at the location defined by the CURR_USER environment variable     
class UserLoginAPI(Resource):
    
    def post(self):
        errors = userLoginScheme.validate(request.json)
        if errors:
            abort(400)
        auth = firebase.auth()
        userInfo = auth.sign_in_with_email_and_password(email, password)
        if userToken == None:
            abort(400)
        
        writeCurrUserInfo(json.dumps(userInfo))
        
        return 'ok'
        
# take iPhone user's token and send it as well as the idToken of the current system to the server, server sends back if the uuid is a match
# if a match, allow user to change room
# if not, abort
class SystemRoomAPI(Resource):
    
    def get(self):
        # check uuid match
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        
        # room_id set in os image to default "room 1"
        roomInfoFile = open(os.environ['ROOM_ID'], "r")
        jsonRoomFile = json.load(roomInfoFile)
        
        return roomInfoFile
    
    def post(self):
        # check uuid match
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        
        errors = systemRoomScheme.validate(request.json["roomID"])
        if errors:
            abort(400)
        
        changeRoomID(request.json['roomID'])
        
        return 'ok'

# take iPhone user's token and send it as well as the idToken of the current system to the server, server sends back if the uuid is a match
# if a match, allow user to check/change status of the system
# if not, abort
class SystemStatusAPI(Resource):
    
    def get(self):
        # check uuid match
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        
        systemStatusInfo = {
            "status": os.environ['CURRENT_STATUS']
        }
        
        return systemStatusInfo
    
    def post(self):
        # check uuid match
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        
        errors = systemInfoScheme.validate(request.form)
        if errors:
            abort(400)
        
        if(request.form['status'] == 'START'):
            os.environ['CURRENT_STATUS'] = 'RUNNING'
            # run CNN code in asych thread
            
        elif(request.form['status'] == 'STOP'):
            os.environ['CURRENT_STATUS'] = 'OFF'
            # kill CNN thread
            
        elif(request.form['status'] == 'RESET'):
            # kill CNN thread
            changeRoomID('room 1')
            deleteCurrUserInfo()
            os.environ['CURRENT_STATUS'] = 'OFF'
            # disconnect from wifi and forget network
            
        return 'ok'

api.add_resource(UserLoginAPI, "/login", endpoint = 'login')
api.add_resource(SystemRoomAPI, "/roomID", endpoint = 'roomID')
api.add_resource(SystemStatusAPI, "/status", endpoint = 'status')

if __name__ == '__main__':
    app.run()