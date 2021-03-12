import socket
from threading import Thread
from serverTemplate import Server
from time import sleep
from datetime import datetime
import sys

SEPARATOR = "<SEPARATOR>"

class RequestServer(Server):
    serverPort = 12001
    serverIP = socket.gethostbyname(socket.gethostname())
    
    def __init__(self):
        super().__init__(RequestServer.serverIP, RequestServer.serverPort)
        self.database = self.authenticateToDatabase('serverNode', '7$dsV!G3D0Oc')
    
    
    # retrieve the newest entry containing the item the user requested
    def queryDatabase(self, object, collection):
        objectProb = "{}Prob".format(object)
        for entry in collection.find({objectProb:1.0}, {objectProb:1, "dateTime":1, "image":1, "roomID":1}).sort("dateTime", -1):
            newestEntry = entry
            break
        
        return newestEntry
    
    def retrieveImage(self, uid, entryPath):
        imageBytes = bytearray()
        with open(entryPath, "rb") as capturedImage:
            imageBytes = capturedImage.read()
        
        return imageBytes
    
    # process run by each thread
    def run(self, connectionSocket, ipAddress):
        threadStop = False
        while True:
            # recieve token + request from connection socket
            incomingRequest = self.recvMessage(connectionSocket)
            print("Item requested from {}: {} at {}".format(ipAddress, incomingRequest, datetime.now()))
            
            # verify token
            
            # switch collections
            # collection = PiServer.goToCollection(uid)
            collection = "camNodeResults"
            
            # query database for entry
            entry = self.queryDatabase(incomingRequest, self.database.collection)
            
            # extract and format necessary information
            requestedInformation = str(entry["dateTime"]) + SEPARATOR + str(entry["roomID"])
            
            # retrieve image from file system
            requestedImage = self.retrieveImage(uid, entry["image"])
            
            # encode and send necessary info
            encodedInformation = requestedInformation.encode()
            self.sendMessage(connectionSocket, encodedInformation)
            
            # send image
            self.sendMessage(connectionSocket, requestedImage)
            
            threadStop = True
            
            if threadStop:
                break
            
        connectionSocket.close()
    
    def listenForUsers(self):
        self.sock.listen(100)
        while True:
            clientConnectionSocket, clientAddress = self.sock.accept()
            clientConnectionSocket.settimeout(60)
            Thread(target = self.run, args = (clientConnectionSocket, clientAddress)).start()

if __name__ == "__main__":
    RequestServer().listenForUsers()
    