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
    
app = Flask(__name__)
api = Api(app)

# set the path to firebase config file to an environment variable
configFile = open(os.environ['FIREBASE_CONFIG'])
firebase = pyrebase.initialize_app(json.load(configFile))
auth = firebase.auth

userLoginScheme = UserLoginSchema()

def writeCurrUserInfo(jsonUserInfo):
    # path = /.creds/.currUser
    with open(os.environ['CURR_USER'], "w+") as file:
        file.write(jsonUserInfo)
        file.close()

# user sends credentials to pi -> pi logs in once -> pi saves the token to the file at the location defined by the CURR_USER environment variable     
class UserLoginAPI(Resource):
    
    def post(self):
        errors = userLoginScheme.validate(request.json)
        if errors:
            abort(400)
        auth = firebase.auth()
        userInfo = auth.sign_in_with_email_and_password(request.json['email'], request.json['password'])
        if userInfo == None:
            abort(400)
        
        writeCurrUserInfo(json.dumps(userInfo))
        os.system('reboot')

api.add_resource(UserLoginAPI, "/login", endpoint = 'login')

if __name__ == '__main__':
    app.run(host='192.168.1.39')