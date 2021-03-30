from flask import Flask, request, Response
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow
from pymongo import MongoClient
from os import mkdir, path
import datetime
import socket
import base64
import matplotlib.pyplot as plt
from dashboard.py import dashboard

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

DATABASE_IP = socket.gethostbyname(socket.gethostname())
DATABASE_PORT = 27017

UPLOAD_FOLDER = './userImgs'
ALLOWED_EXTENSIONS = set(['jpeg'])

class PiDataPostSchema(ma.Schema):
    userID = fields.Str()
    dateTime = fields.Str()
    roomID = fields.Int()
    keysProb = fields.Decimal()
    glassesProb = fields.Decimal()
    thermosProb = fields.Decimal()
    # image = fields.

class PiDataGetSchema(ma.Schema):
    userID = fields.Str(required = True)
    objectQueried = fields.Str(required = True)
    queryTime = fields.DateTime(required = True)
    

class UserDashboardSchema(ma.Schema):
    userID = fields.Str(required = True)

piDataGetScheme = PiDataGetSchema()
userDashboardScheme = UserDashboardSchema()    

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def authenticateToDatabase():
        mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_IP, DATABASE_PORT))
        
        try:
            rPiDatabase = mongo_client.rPiData
            rPiDatabase.authenticate(name = 'serverNode', password = '7$dsV!G3D0Oc')
            rPiDatabaseCollection = rPiDatabase.camNodeResults
        except:
            raise Exception('Authentication Failed')
        
        return rPiDatabaseCollection
    
# retrieve the newest entry containing the item the user requested
def queryDatabase(collection, form):
    objectProb = "{}Prob".format(form["objectQueried"])
    newestEntry = None
    for entry in collection.find({"$and": [{"userID": form[uid]}, {objectProb:1.0}]}).sort("dateTime", -1):
        newestEntry = entry
        break
        
    if newestEntry != None:
        mornQuery = 0
        afterQuery = 0
        evenQuery = 0
        
        currentTime = datetime.now()
        mornStart = datetime.datetime(datetime.date.year, datetime.date.month, datetime.date.day, 5, 0, 0, 0)
        mornEnd = datetime.datetime(datetime.date.year, datetime.date.month, datetime.date.day, 11, 59, 59, 99)
        afterStart = datetime.datetime(datetime.date.year, datetime.date.month, datetime.date.day, 12, 0, 0, 0)
        afterEnd = datetime.datetime(datetime.date.year, datetime.date.month, datetime.date.day, 17, 59, 59, 99)
        
        if(mornStart <= currentTime and currentTime <= mornEnd):
            morningQuery = 1
        elif(afterStart <= currentTime and curretTime <= afterEnd):
            afterQuery = 1
        else:
            evenQuery = 1
            
        # insert instance of queried object for dashboard purposes
        collection.insert_one({
            "userID" : form["userID"],
            "objectQueried" : form["objectQueried"],
            "queriedDateTime" : form["queriedDateTime"],
            "morningQuery": mornQuery,
            "afterQuery": afterQuery,
            "evenQuery": evenQuery
        })

    return newestEntry

 # saves image to file system and adds image path to entry
def saveImage(entry, imageData):
    userPath = "./userImgs/{}".format(entry["userID"])
    if path.isdir(userPath) == False:
        mkdir(userPath)
            
    imgPath = "./userImgs/{}/{}_{}.jpg".format(entry["userID"], entry["roomID"], entry["dateTime"])
        
    imageData.save(imgPath)
        
    return imgPath

def retrieveImage(entryPath):
        imageBytes = bytearray()
        with open(entryPath, "rb") as capturedImage:
            imageBytes = capturedImage.read()
        
        return imageBytes
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# post: allows users to login and receive a token
class LoginAPI(Resource):
    def post(self):
        pass

# get: allows users to get entry info on the apple apps and alexas
# post: allows pis to insert entries into database
class PiDataAPI(Resource):
    decorators = []
    
    # NEED TO FINISH
    def get(self):
        print("Sending!")
        errors = piDataGetScheme.validate(request.form)
        if errors:
            abort(400)
        db = authenticateToDatabase()
        entry = queryDatabase(db, request.form)
        imageData = retrieveImage(entry["image"])
        
        return entry
        
    
    def post(self):
        print("Received!")
        args = self.reqparse.parse_args()
        print(request.form)
        
        entry = request.form.to_dict()
        if "image" not in request.files:
            abort(400)
            
        imageData = request.files['image']
        
        if imageData.filename == '':
            abort(400)
        if imageData and allowed_file(imageData.filename):
            db = authenticateToDatabase()
            imgPath = saveImage(entry, imageData)
            entry["image"] = imgPath
            db.insert_one(entry)
        
        return 'ok'

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
        errors = userDashboardScheme.validate(request.form)
        if errors:
            abort(400)
        
        db = authenticateToDatabase()
        mornQueries = db.find({})
        dashboard(db)
        

api.add_resource(PiDataAPI, "/pidata", endpoint = 'pidata')
api.add_resource(UserDashboardAPI, "/dashboard", endpoint = 'dashboard')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")