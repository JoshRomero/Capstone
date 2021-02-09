from pymongo import MongoClient
from base64 import b64decode

# host machine ip and mongodb port
DATABASE_DOMAIN = '192.168.1.54'
DATABASE_PORT = 27017

def queryDatabase(object):
    # retrieve the newest document from the collection based on datetime (will be changed later to include CNN results)
    for entry in camNodeResultsCollection.find().sort("dateTime", -1):
        newestEntry = entry
        break
    
    # retrieve the image data and date time
    encryptedImageData = newestEntry["image"]
    dateAndTime = newestEntry["dateTime"]

    # unencrypt b64 encrypted image data
    unencryptedImageData = b64decode(encryptedImageData)

    # save unencrypted image to a folder known as serverImgs
    with open('../serverImgs/{}.jpeg'.format(dateAndTime), mode='wb') as newImage:
        unencryptedImageData = bytearray(unencryptedImageData)
        newImage.write(unencryptedImageData)
        print("[+] Entry image saved in serverImgs folder with name: {}.jpeg".format(dateAndTime))
        newImage.close()
        
# MAIN

# connect to the server
try:
    print("[+] Connecting to mongoDB server @ {}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    print("[+] Connected")
except:
    print("[-] Connection failed")
    exit(0)

# authenticate to database
try:
    rPiDatabase = mongo_client.rPiData
    print("[+] Authenticating to rPiData database...")
    rPiDatabase.authenticate(name='serverNode', password='7$dsV!G3D0Oc')
    print("[+] Sucessfully Authenticated")
except:
    print("[-] Authentication failed")
    exit(0)

# switch to correct collection
try:
    print("[+] Switching to camNodeResults collection...")
    camNodeResultsCollection = rPiDatabase.camNodeResults
    print("[+] Successfully switched")
except:
    print("[-] Switch failed")