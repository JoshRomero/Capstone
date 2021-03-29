from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from pymongo import MongoClient
from os import mkdir, path
from datetime import datetime
import socket

app = Flask(__name__)
api = Api(app)

DATABASE_IP = socket.gethostbyname(socket.gethostname())
DATABASE_PORT = 27017

def authenticateToDatabase():
        mongo_client = MongoClient("mongodb://{}:{}".format(SERVER_IP, SERVER_PORT))
        
        try:
            rPiDatabase = mongo_client.rPiData
            rPiDatabase.authenticate(name = user, password = password)
            rPiDatabaseCollection = rPiDatabase.camNodeResults
        except:
            raise Exception('Authentication Failed')
        
        return rPiDatabase
    
# retrieve the newest entry containing the item the user requested
def queryDatabase(object, collection, uid):
    objectProb = "{}Prob".format(object)
    newestEntry = None
    for entry in collection.find({"$and": [{"userID": uid}, {objectProb:1.0}]}).sort("dateTime", -1):
        newestEntry = entry
        break
        
    if newestEntry != None:
            
        # insert query information into collection for dashboard
        collection.insert_one({"objectQueried": object})

    return newestEntry

 # saves image to file system and adds image path to entry
def saveImage(args):
    userPath = "./userImgs/{}".format(args["userID"])
    if path.isdir(userPath) == False:
        mkdir(userPath)
            
    imgPath = "./userImgs/{}/{}_{}.jpg".format(args["userID"], args["roomID"], args["dateTime"])
        
    with open(imgPath, "wb+") as capturedImage:
        capturedImage.write(args["image"])
        
    return imgPath

def retrieveImage(entryPath):
        imageBytes = bytearray()
        with open(entryPath, "rb") as capturedImage:
            imageBytes = capturedImage.read()
        
        return imageBytes

# post: allows users to login and receive a token
class LoginAPI(Resource):
    def post(self):
        pass

# get: allows users to get entry info on the apple apps and alexas
# post: allows pis to insert entries into database
class PiDataAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userID', type = str, required = True, location = 'json')
        self.reqparse.add_argument('roomID', type = str, required = True, location = 'json')
        self.reqparse.add_argument('image', type = bytes, required = True, location = 'json')
        super(PiDataAPI, self).__init__()
        
    def get(self, userID, item):
        print("Sending!")
        db = authenticateToDatabase()
        entry = self.queryDatabase(item, db, userID)
        
        return entry
        
    
    def post(self, userID, item):
        print("Received!")
        content = request.json
        print(content)
         
        # args = self.reqparse.parse_args()
        # db = authenticateToDatabase()
        # imagePath = saveImage(args)
        # content["image"] = imagePath
        # db.insert_one(content)

# get: tells user information about the devices that are associated with their account
# post: allows users to register new pi devices
# put: allows users to change pi room id
# delete: allows users to remove a pi from their registered devices
class UserDevicesAPI(Resource):
    def get(self):
        pass
    
    def post(self):
        pass
    
    def put(self):
        pass
    
    def delete(self):
        pass

# display dashboard of information for all user requests
class DashboardAPI(Resource):
    def get(self):
        pass

# display dashboard of information for a specific user's requests
class UserDashboardAPI(Resource):
    def get(self):
        pass

api.add_resource(PiDataAPI, "/<string:userID>/pidata/<string:item>", endpoint='pidata')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")