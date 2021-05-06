# webserver imports
from flask import Flask, request
from flask_restful import abort, Api, Resource
from marshmallow import fields, Schema
import json
import os
import requests
from multiprocessing import Process
from getmac import get_mac_address

class SystemRoomSchema(Schema):
    roomID = fields.Str()

class SystemStatusSchema(Schema):
    status = fields.Str()
    
app = Flask(__name__)
api = Api(app)

systemRoomScheme = SystemRoomSchema()
systemStatusScheme = SystemStatusSchema()

def runTokenRefresh():
    os.system("python3 /home/pi/tflite1/refreshToken.py")

def runNeuralNetwork():
    os.system("python3 /home/pi/tflite1/imageFinal.py --modeldir=Sample_TFlite_model")

# remove user info file
def deleteCurrUserInfo():
    with open(os.environ['CURR_USER'], 'w') as file:
        pass

def getIdToken():
    user = open(os.environ['CURR_USER'], "r")
    jsonUser = json.loads(user.read())
    try:
        idToken = jsonUser["idToken"]
        return idToken
    except:
        getIdToken()

# send a post request to server containing the iPhone's idToken and the current Pi's idToken to compare uids 
def compareUUIDs(iphoneIdToken):
    header = {"Authorization": getIdToken()}
    payload = {"idToken": iphoneIdToken}
    url = "https://objectfinder.tech/compare/userids"
    r = requests.post(url, json=payload, headers=header)
    rDict = json.loads(r.text)
        
    if rDict["equivalentUIDS"] == "true":
        return True
    else:
        return False

# write user defined roomID to the roomID info file
def changeRoomID(newRoomID):
    systemRoomInfo = {"roomID": newRoomID}
    with open(os.environ['ROOM_ID'], 'w') as file:
        file.write(json.dumps(systemRoomInfo))
        file.close()

# write status to the current status file
# path = /.creds/status.json       
def writeCurrStatusInfo(newStatus):
    newStatusJson = {"status": newStatus}
    with open(os.environ['CURR_STATUS'], "w") as file:
        file.write(json.dumps(newStatusJson))
        file.close()
        
def sendIpToServer():
    header = {"Authorization": getIdToken()}
    payload = {"macAddress": get_mac_address(), "ipAddress": socket.gethostbyname(socket.gethostname() + ".local")}
    url = "https://objectfinder.tech/pi/update"
    requests.post(url, json=payload, headers=header)

def removeMacFromServer():
    header = {"Authorization": getIdToken()}
    payload = {"macAddress": get_mac_address()}
    url = "https://objectfinder.tech/mac/remove"
    request.post(url, json=payload, headers=header)
        
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
        
        return jsonRoomFile
    
    def post(self):
        token = request.headers["Authorization"]
        if compareUUIDs(token) == False:
            abort(401)
        data = request.form.to_dict()
        for key in data.items():
            data = json.loads(key[0])
        errors = systemRoomScheme.validate(request.json)
        if errors:
            abort(400)
        
        changeRoomID(data['roomID'])
        
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
        
        data = request.form.to_dict()
        for key in data.items():
            data = json.loads(key[0])
        errors = systemStatusScheme.validate(data)
        if errors:
            abort(400)
        
        # kill CNN and token refresh processes, reset userInfo and roomID defaults
        if(data['status'] == 'RESET'):
            writeCurrStatusInfo('RESET')
            neuralNetworkProcess.join()
            reTokenProcess.join()
            changeRoomID('DEFAULT')
            removeMacFromServer()
            deleteCurrUserInfo()
            
            # disconnect from wifi and forget network
            os.system('rm /etc/NetworkManager/system-connections/*')
            os.system('reboot')
        elif(data['status'] == 'RESTART'):
            writeCurrStatusInfo('RESTART')
            reTokenProcess.join()
            neuralNetworkProcess.join()
            os.system('reboot')

api.add_resource(SystemRoomAPI, "/roomID", endpoint = 'roomID')
api.add_resource(SystemStatusAPI, "/status", endpoint = 'status')

if __name__ == '__main__':
    writeCurrStatusInfo('ACTIVE')
    
    reTokenProcess = Process(target=runTokenRefresh, args=())
    reTokenProcess.start()
    neuralNetworkProcess = Process(target=runNeuralNetwork, args=())
    neuralNetProcess.start()
    sendIpToServer()
    
    app.run('0.0.0.0')