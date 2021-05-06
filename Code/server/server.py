from flask import Flask, request, send_from_directory
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
UPLOAD_FOLDER = '/userImgs'
ALLOWED_EXTENSIONS = set(['jpg'])

class PiDataPostSchema(Schema):
    userID = fields.Str()
    dateTime = fields.Str()
    roomID = fields.Str()
    remoteProb = fields.Decimal()
    laptopProb = fields.Decimal()
    cellphoneProb = fields.Decimal()
    handbagProb = fields.Decimal()
    bookProb = fields.Decimal()

class PiDataGetSchema(Schema):
    object = fields.Str(required = True)

class PiDataImageGetSchema(Schema):
    dateTime = fields.Str()

class CompareUserIdPostSchema(Schema):
    idToken = fields.Str()

class PiRegistrationPostSchema(Schema):
    deviceMac = fields.Str()

class PiIpUpdatePostSchema(Schema):
    macAddress = fields.Str()
    ipAddress = fields.Str()

app = Flask(__name__)
api = Api(app)

cred = credentials.Certificate(os.environ['FIREBASE_CREDENTIALS'])
firebase = firebase_admin.initialize_app(cred)

piDataPostScheme = PiDataPostSchema()
piDataGetScheme = PiDataGetSchema()
piDataImageGetScheme = PiDataImageGetSchema()
compareUserIdPostScheme = CompareUserIdPostSchema()
piRegistrationPostScheme = PiRegistrationPostSchema()
piIpUpdatePostScheme = PiIpUpdatePostSchema()

def authenticateToDatabase():
        mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_IP, DATABASE_PORT))

        try:
            rPiDatabase = mongo_client.rPiData
            rPiDatabase.authenticate(name = os.environ['DATABASE_USER'], password = os.environ['DATABASE_PASS'])
        except:
            raise Exception('Authentication Failed')

        return rPiDatabase

def formatEntries(dbEntry, args):
    formattedEntry = {
            "dateTime": dbEntry["dateTime"],
            "roomID": dbEntry["roomID"],
            "itemFound": args["object"].lower()
            }

    return formattedEntry

# retrieve the newest entry containing the item the user requested
def queryDatabaseItem(collection, args, userID):
    objectProb = "{}Prob".format(args["object"].lower())
    newestEntry = None
    for entry in collection.find({'$and':[{"userID": userID},{objectProb:"1.0"}]}).sort("dateTime", -1):
        newestEntry = entry
        break

    # return 404 error if resource cannot be found
    if newestEntry == None:
        return abort(404)

    formattedEntry = formatEntries(newestEntry, args)

    return formattedEntry

def queryDatabasePi(collection, userID):
    for entry in collection.find({"userID": userID}):
        return entry

    return None

def registerUserPi(collection, userID, macAddress):
    userEntry = queryDatabasePi(collection, userID)
    if userEntry == None:
        entry = {"userID": userID,
                "devices": {
                    macAddress: ""
                    }
                }
        collection.insert_one(entry)
    elif(userEntry['devices'][macAddress] != None):
       return 'Already Registered'
    else:
        deviceKey = "devices.{}".format(macAddress)
        collection.update({"userID": userID}, {"$set": {deviceKey: ""}})

def removeUserPi(collection, userID, macAddress):
    userEntry = queryDatabasePi(collection, userID)
    deviceKey = "devices.{}".format(macAddress)
    collection.update({"userID": userID}, {"$unset": {deviceKey: None}}, multi = True)

def updatePiIp(collection, userID, macAddress, currentIP):
    deviceKey = "devices.{}".format(macAddress)
    collection.update({"userID": userID}, {"$set": {deviceKey: currentIP}})

# saves image to file system and adds image path to entry
def saveImage(entry, imageData, userID):
    userPath = os.path.join(UPLOAD_FOLDER,  userID)
    if os.path.isdir(userPath) == False:
        os.makedirs(userPath)

    imgPath = os.path.join(userPath, entry["dateTime"] + ".jpg")
    imageData.save(imgPath)

    return imgPath

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verifyToken(token):
    decoded_token = auth.verify_id_token(token)
    if decoded_token:
        uid = decoded_token['uid']
    else:
        # return http status code for bad login
        abort(401)

    return uid

# get: allows users to get entry info on the apple apps and alexas
# post: allows pis to insert entries into database
class PiDataAPI(Resource):

    def get(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)
        errors = piDataGetScheme.validate(request.args)
        print("ARGS: " , request.args)
        if errors:
            abort(400)
        print("NO ERRORS")
        db = authenticateToDatabase().camNodeResults
        print("AUTHENTICATED")
        formattedEntry = queryDatabaseItem(db, request.args, uid)

        return formattedEntry

    def post(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)

        errors = piDataPostScheme.validate(request.form)
        if errors:
            abort(400)
        entry = request.form.to_dict()

        if "image" not in request.files:
            abort(400)
        imageData = request.files['image']
        if imageData.filename == '':
            abort(400)
        if imageData and allowed_file(imageData.filename):
            db = authenticateToDatabase().camNodeResults
            entry["dateTime"] = entry["dateTime"].replace(" ", "_")
            imgPath = saveImage(entry, imageData, uid)
            entry["image"] = imgPath
            db.insert_one(entry)

        return 'ok'

class PiDataImageAPI(Resource):

    def get(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)
        errors = piDataImageGetScheme.validate(request.args)
        if errors:
            abort(400)

        return send_from_directory(os.path.join(UPLOAD_FOLDER,  uid), request.args["dateTime"] + '.jpg',  as_attachment=True)

class CompareUserIdAPI(Resource):

    def post(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)
        print(request.json)
        errors = compareUserIdPostScheme.validate(request.json)
        if errors:
            abort(400)

        otherUid = verifyToken(request.json["idToken"])
        result = {}

        if uid == otherUid:
            result["equivalentUIDS"] = "true"
        else:
            result["equivalentUIDS"] = "false"

        return result

class RegisterPiMacAPI(Resource):

    def post(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)

        errors = piRegistrationPostScheme.validate(request.json)
        if errors:
            abort(400)

        db = authenticateToDatabase().registeredPis
        registerUserPi(db, uid, request.json["deviceMac"])

        return 'ok'

class RemovePiMacAPI(Resource):

    def post(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)

        errors = piRegistrationPostScheme.validate(request.json)
        if errors:
            abort(400)

        db = authenticateToDatabase().registeredPis
        removeUserPi(db, uid, request.json["deviceMac"])

        return 'ok'

class UpdatePiIpAPI(Resource):

    def post(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)

        errors = piIpUpdatePostScheme.validate(request.json)
        if errors:
            abort(400)

        db = authenticateToDatabase().registeredPis
        updatePiIp(db, uid, request.json["macAddress"], request.json["ipAddress"])

        return 'ok'

class PiDevicesAPI(Resource):
    def get(self):
        token = request.headers["Authorization"]
        uid = verifyToken(token)

        db = authenticateToDatabase().registeredPis
        userEntry = queryDatabasePi(db, uid)

        return userEntry["devices"]

api.add_resource(PiDataAPI, '/pidata', endpoint = 'pidata')
api.add_resource(PiDataImageAPI, '/pidata/image', endpoint = 'image')
api.add_resource(CompareUserIdAPI, '/compare/userids', endpoint = 'userid')
api.add_resource(RegisterPiMacAPI, '/mac/register', endpoint = 'register')
api.add_resource(RemovePiMacAPI, '/mac/remove', endpoint = 'remove')
api.add_resource(UpdatePiIpAPI, '/ip/update', endpoint = 'update')
api.add_resource(PiDevicesAPI, '/devices', endpoint = 'devices')

if __name__ == '__main__':
    app.run()
~