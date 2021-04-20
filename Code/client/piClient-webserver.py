# webserver imports
from flask import Flask, request
from flask_restful import abort, Api, Resource
from marshmallow import fields, Schema
import pyrebase
import json
import os

class WirelessLoginSchema(Schema):
    ssid = fields.str()
    psk = fields.str()

class UserLoginSchema(Schema):
    email = fields.Str()
    password = fields.Str()

class SystemRoomSchema(Schema):
    room = fields.str()

class SystemStatusSchema(Schema):
    status = fields.str()
    
app = Flask(__name__)
api = Api(app)

# set the path to firebase config file to an environment variable
configFile = open(os.environ['FIREBASE_CONFIG'])
firebase = pyrebase.initialize_app(json.load(configFile))

wirelessLoginScheme = WirelessLoginSchema()
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
        
        # room_id set in os image to default "room 1"
        systemRoomInfo = {
            "roomID": os.environ['ROOM_ID']
        }
        return systemRoomInfo
    
    def post(self):
        # check uuid match
        
        errors = systemRoomScheme.validate(request.form)
        if errors:
            abort(400)
        os.environ['ROOM_ID'] = request.form['roomID']
        
        return 'ok'

# take iPhone user's token and send it as well as the idToken of the current system to the server, server sends back if the uuid is a match
# if a match, allow user to check/change status of the system
# if not, abort
class SystemStatusAPI(Resource):
    
    def get(self):
        # check uuid match
        
        systemStatusInfo = {
            "status": os.environ['CURRENT_STATUS']
        }
        
        return systemStatusInfo
    
    def post(self):
        # check uuid match
        
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
            os.environ['ROOM_ID'] = 'Room 1'
            deleteCurrUserInfo()
            os.environ['CURRENT_STATUS'] = 'OFF'
            # disconnect from wifi and forget network
            
        return 'ok'

api.add_resource(WirelessConnectionAPI, "/wifi", endpoint = 'wifi')
api.add_resource(UserLoginAPI, "/login", endpoint = 'login')
api.add_resource(SystemRoomAPI, "/roomID", endpoint = 'roomID')
api.add_resource(SystemStatusAPI, "/status", endpoint = 'status')

if __name__ == '__main__':
    app.run()