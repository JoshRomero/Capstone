from flask import Flask, request
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from marshmallow import fields, Schema
from pymongo import MongoClient
import os
import datetime
import socket
import matplotlib.pyplot as plt
from dashboard import dashboard
import json
import firebase_admin
from firebase_admin import auth, credentials
import requests

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
    remoteProb = fields.Decimal()

class PiDataGetSchema(Schema):
    objectQueried = fields.Str(required = True)

class ReturnedQuerySchema(Schema):
    dateTime = fields.Str()
    roomID = fields.Str()
    itemFound = fields.Str()

app = Flask(__name__)
api = Api(app)

cred = credentials.Certificate(os.environ['FIREBASE_CREDENTIALS'])
firebase = firebase_admin.initialize_app(cred)

piDataPostScheme = PiDataPostSchema()
piDataGetScheme = PiDataGetSchema()
returnedQueryScheme = ReturnedQuerySchema()

def authenticateToDatabase():
        mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_IP, DATABASE_PORT))

        try:
            rPiDatabase = mongo_client.rPiData
            rPiDatabase.authenticate(name = os.environ['DATABASE_USER'], password = os.environ['DATABASE_PASS'])
            rPiDatabaseCollection = rPiDatabase.camNodeResults
        except:
            raise Exception('Authentication Failed')

        return rPiDatabaseCollection

def formatEntries(dbEntry, args):
    formattedEntry = {
            "dateTime": dbEntry["dateTime"],
            "roomID": dbEntry["roomID"],
            "itemFound": args["objectQueried"].lower()
            }

    return formattedEntry

# retrieve the newest entry containing the item the user requested
def queryDatabase(collection, args, userID):
    objectProb = "{}Prob".format(args["objectQueried"].lower())
    newestEntry = None
    for entry in collection.find({'$and':[{"userID": userID},{objectProb:"1.0"}]}).sort("dateTime", -1):
        newestEntry = entry
        break

    # return 404 error if resource cannot be found
    if newestEntry == None:
        return abort(404)

    formattedEntry = formatEntries(newestEntry, args)
    # insert instance of queried object for dashboard purposes
    #mornQuery = 0
    #afterQuery = 0
    #evenQuery = 0

    #currentTime = datetime.datetime.now()
    #currentDay = datetime.datetime.today()
    #mornStart = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 5, 0, 0, 0)
    #mornEnd = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 11, 59, 59, 99)
    #afterStart = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 12, 0, 0, 0)
    #afterEnd = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 17, 59, 59, 99)

    #if(mornStart <= currentTime and currentTime <= mornEnd):
    #    morningQuery = 1
    #elif(afterStart <= currentTime and currentTime <= afterEnd):
    #    afterQuery = 1
    #else:
    #    evenQuery = 1

   # collection.insert_one({
   #     "userID" : args["userID"],
   #     "objectQueried" : args["objectQueried"].lower(),
   #     "queriedDateTime" : currentTime,
   #     "morningQuery": mornQuery,
   #     "afterQuery": afterQuery,
   #     "evenQuery": evenQuery
   # })

    return formattedEntry, newestEntry["image"]

# saves image to file system and adds image path to entry
def saveImage(entry, imageData, userID):
    userPath = os.path.join(app.root_path, userID)
    if os.path.isdir(userPath) == False:
        os.makedirs(userPath)

    imgPath = os.path.join(userPath, entry["dateTime"])
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

def verifyToken(token):
    decoded_token = auth.verify_id_token(token)
    print("decoded token: ", decoded_token)
    if decoded_token:
        uid = decoded_token['uid']
    else:
        # return http status code for bad login
        abort(401)

    return uid

# get: allows users to get entry info on the apple apps and alexas
# post: allows pis to insert entries into database
class PiDataAPI(Resource):

    # NEED TO FINISH -- figure out how to send image data and json at the same time
    def get(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)
        errors = piDataGetScheme.validate(request.args)
        if errors:
            abort(400)
        db = authenticateToDatabase()
        formattedEntry, imgPath = queryDatabase(db, request.args, uid)
        # imageData = retrieveImage(imgPath)
        return formattedEntry

    def post(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)

        errors = piDataPostScheme.validate(request.form)
        if errors:
            abort(400)
        entry = request.form.to_dict()
        print("Entry:", entry)
        if "image" not in request.files:
            abort(400)
        imageData = request.files['image']
        if imageData.filename == '':
            abort(400)
        if imageData and allowed_file(imageData.filename):
            db = authenticateToDatabase()
            imgPath = saveImage(entry, imageData, uid)
            entry["image"] = imgPath
            db.insert_one(entry)

        return 'ok'

# display dashboard of information for a specific user's requests
class UserDashboardAPI(Resource):
    def get(self):
        #uid = verifyToken(request.headers["Authorization"])

        db = authenticateToDatabase()
        return("authenticated")
       # dashboard(db)

api.add_resource(PiDataAPI, "/pidata", endpoint = 'pidata')
api.add_resource(UserDashboardAPI, "/dashboard", endpoint = 'dashboard')

if __name__ == '__main__':
    app.run()