# webserver imports
from flask import Flask, request
from flask_restful import abort, Api, Resource
from marshmallow import fields, Schema
import pyrebase
import json
import os
import requests
from getmac import get_mac_address

class UserLoginSchema(Schema):
    email = fields.Str()
    password = fields.Str()
    roomID = fields.Str()
    
app = Flask(__name__)
api = Api(app)

# set the path to firebase config file to an environment variable
configFile = open(os.environ['FIREBASE_CONFIG'])
firebase = pyrebase.initialize_app(json.load(configFile))
auth = firebase.auth

userLoginScheme = UserLoginSchema()

# path = /.creds/.currUser
def writeCurrUserInfo(jsonUserInfo):
    with open(os.environ['CURR_USER'], "w+") as file:
        file.write(jsonUserInfo)
        file.close()

# write user defined roomID to the roomID info file
def changeRoomID(newRoomID):
    systemRoomInfo = json.dumps({"roomID": newRoomID})
    with open(os.environ['ROOM_ID'], 'w') as file:
        file.write(systemRoomInfo)
        file.close()

def sendMacToServer(currentMac, currentName, idToken):
    header = {"Authorization": idToken}
    payload = {"deviceMac": currentMac, "deviceName": currentName}
    url = "https://objectfinder.tech/register"
    requests.post(url, json=payload, headers=header)
    
# user sends credentials to pi -> pi logs in once -> pi saves the token to the file at the location defined by the CURR_USER environment variable     
class UserLoginAPI(Resource):
    
    def post(self):
        data = request.form.to_dict()
        for key in data.items():
            data = json.loads(key[0])
        errors = userLoginScheme.validate(data)
        if errors:
            abort(400)
            
        auth = firebase.auth()
        userInfo = auth.sign_in_with_email_and_password(data['email'], data['password'])
        if userInfo == None:
            abort(400)
        print("WRITING USER INFO")
        writeCurrUserInfo(json.dumps(userInfo))
        
        print("SENDING MAC")
        sendMacToServer(get_mac_address(), data['roomID'], userInfo["idToken"])
        
        print("CHANGING ROOMID")
        changeRoomID(data['roomID'])
        
        os.system('reboot')

api.add_resource(UserLoginAPI, "/register", endpoint = 'register')

if __name__ == '__main__':
    app.run(host='0.0.0.0')