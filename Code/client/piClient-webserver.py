# webserver imports
from flask import Flask, request
from flask_restful import abort, Api, Resource
from marshmallow import fields, Schema
import json
import os
import requests
from multiprocessing import Process

class SystemRoomSchema(Schema):
    room = fields.Str()

class SystemStatusSchema(Schema):
    status = fields.Str()
    
app = Flask(__name__)
api = Api(app)

systemRoomScheme = SystemRoomSchema()
systemStatusScheme = SystemRoomSchema()

def runTokenRefresh():
    import refreshToken

def runNeuralNetwork():
    import imageFinal

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

# write status to the current status file       
def writeCurrStatusInfo(newStatus):
    # path = /.creds/status.json
    newStatusJson = {"status": newStatus}
    with open(os.environ['CURR_STATUS'], "w") as file:
        file.write(newStatusJson)
        file.close()
        
# take iPhone user's token and send it as well as the idToken of the current system to the server, server sends back if the uuid is a match
# if a match, allow user to change room
# if not, abort
class SystemRoomAPI(Resource):
    
    def get(self):
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        
        # room_id set in os image to default "room 1"
        roomInfoFile = open(os.environ['ROOM_ID'], "r")
        jsonRoomFile = json.load(roomInfoFile)
        
        return roomInfoFile
    
    def post(self):
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
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
            
        statusFile = open(os.environ['CURR_STATUS'], "r")
        jsonStatusFile = json.load(statusFile)
        
        return jsonStatusFile
    
    def post(self):
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        
        errors = systemStatusScheme.validate(request.form)
        if errors:
            abort(400)
        
        # begin neural network code process
        if(request.form['status'] == 'START'):
            writeCurrStatusInfo('ACTIVE')
        
        # kill neural network code process
        elif(request.form['status'] == 'STOP'):
            writeCurrStatusInfo('INACTIVE')
            neuralNetProcess.join()
        
        # kill CNN and token refresh processes, reset userInfo and roomID defaults
        elif(request.form['status'] == 'RESET'):
            writeCurrStatusInfo('INACTIVE')
            neuralNetProcess.join()
            reTokenProcess.join()
            changeRoomID('DEFAULT')
            deleteCurrUserInfo()
            
            # disconnect from wifi and forget network
            os.system('rm /etc/NetworkManager/system-connections/*')
            os.system('reboot')
            
        return 'ok'

api.add_resource(SystemRoomAPI, "/roomID", endpoint = 'roomID')
api.add_resource(SystemStatusAPI, "/status", endpoint = 'status')

if __name__ == '__main__':
    # begin refresh code in asynch process
    reTokenProcess = Process(target=runTokenRefresh, args=())
    
    # begin neural network code in asynch process
    neuralNetProcess = Process(target=runNeuralNetwork, args=())
    
    app.run()