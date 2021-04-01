from flask import Flask, request, Response
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from marshmallow import fields, Schema
from pymongo import MongoClient
from os import mkdir, path
import datetime
import socket
import base64
import matplotlib.pyplot as plt
from dashboard import dashboard
import json

DATABASE_IP = socket.gethostbyname(socket.gethostname())
DATABASE_PORT = 27017
UPLOAD_FOLDER = './userImgs'
ALLOWED_EXTENSIONS = set(['jpeg'])

class PiDataPostSchema(Schema):
    userID = fields.Str()
    dateTime = fields.Str()
    roomID = fields.Int()
    keysProb = fields.Decimal()
    glassesProb = fields.Decimal()
    thermosProb = fields.Decimal()

class PiDataGetSchema(Schema):
    userID = fields.Str(required = True)
    objectQueried = fields.Str(required = True)

class UserDashboardSchema(Schema):
    userID = fields.Str(required = True)

class ReturnedQuerySchema(Schema):
    userID = fields.Str()
    dateTime = fields.Str()
    roomID = fields.Str()
    itemFound = fields.Str()

app = Flask(__name__)
api = Api(app)
piDataPostScheme = PiDataPostSchema()
piDataGetScheme = PiDataGetSchema()
userDashboardScheme = UserDashboardSchema()
returnedQueryScheme = ReturnedQuerySchema()

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

def formatEntries(dbEntry, args):
    if dbEntry == None:
        formattedEntry = {
            "userID": args["userID"],
            "dateTime": "None",
            "roomID": "None",
            "itemFound": "None"
            }

        return formattedEntry

    formattedEntry = {
            "userID": dbEntry["userID"],
            "dateTime": dbEntry["dateTime"],
            "roomID": dbEntry["roomID"],
            "itemFound": args["objectQueried"].lower()
            }

    return formattedEntry

# retrieve the newest entry containing the item the user requested
def queryDatabase(collection, args):
    objectProb = "{}Prob".format(args["objectQueried"].lower())
    newestEntry = None
    for entry in collection.find({'$and':[{"userID": args["userID"]},{objectProb:"1.0"}]}).sort("dateTime", -1):
        newestEntry = entry
        break

    if newestEntry == None:
        formattedEntry = formatEntries(newestEntry, args)

        return formattedEntry, None

    formattedEntry = formatEntries(newestEntry, args)

    # insert instance of queried object for dashboard purposes
    mornQuery = 0
    afterQuery = 0
    evenQuery = 0

    currentTime = datetime.datetime.now()
    currentDay = datetime.datetime.today()
    mornStart = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 5, 0, 0, 0)
    mornEnd = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 11, 59, 59, 99)
    afterStart = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 12, 0, 0, 0)
    afterEnd = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 17, 59, 59, 99)

    if(mornStart <= currentTime and currentTime <= mornEnd):
        morningQuery = 1
    elif(afterStart <= currentTime and currentTime <= afterEnd):
        afterQuery = 1
    else:
        evenQuery = 1

    collection.insert_one({
        "userID" : args["userID"],
        "objectQueried" : args["objectQueried"].lower(),
        "queriedDateTime" : currentTime,
        "morningQuery": mornQuery,
        "afterQuery": afterQuery,
        "evenQuery": evenQuery
    })

    return formattedEntry, newestEntry["image"]

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

    # NEED TO FINISH -- figure out how to send image data and json at the same time
    def get(self):
        errors = piDataGetScheme.validate(request.args)
        if errors:
            abort(400)
        db = authenticateToDatabase()
        formattedEntry, imgPath = queryDatabase(db, request.args)
        if formattedEntry["itemFound"] != "None":
            imageData = retrieveImage(imgPath)

        return json.dumps(formattedEntry)

    def post(self):
        errors = piDataPostScheme(request.form)
        if errors:
            abort(400)
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
        dashboard(db)


api.add_resource(PiDataAPI, "/pidata", endpoint = 'pidata')
api.add_resource(UserDashboardAPI, "/dashboard", endpoint = 'dashboard')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=12001)