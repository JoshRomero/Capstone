import socket
from threading import Thread
from serverTemplate import Server
from datetime import datetime

SEPARATOR = "<SEPARATOR>"

class RequestServer(Server):
    serverPort = 12001
    serverIP = socket.gethostbyname(socket.gethostname())
    
    def __init__(self):
        super().__init__(RequestServer.serverIP, RequestServer.serverPort)
        self.database = self.authenticateToDatabase('serverNode', '7$dsV!G3D0Oc')
    
    
    # retrieve the newest entry containing the item the user requested
    def queryDatabase(self, object, collection, uid):
        objectProb = f"{object}Prob"
        for entry in collection.find({"userID": uid, objectProb:1.0}, {objectProb:1, "dateTime":1, "image":1, "roomID":1}).sort("dateTime", -1):
            newestEntry = entry
            break
        
        return newestEntry
    
    def retrieveImage(self, entryPath):
        imageBytes = bytearray()
        with open(entryPath, "rb") as capturedImage:
            imageBytes = capturedImage.read()
        
        return imageBytes
    
    # process run by each thread
    def run(self, connectionSocket, ipAddress):
        threadStop = False
        while True:
            # receive token
            
            # verify token
            
            # receive request from connection socket
            incomingRequest = self.recvMessage(connectionSocket)
            print(f"Item requested from {ipAddress}: {incomingRequest} at {datetime.now()}")
            
            # query database for entry
            collection = self.database.self.collection
            entry = self.queryDatabase(incomingRequest, collection, uid)
            
            # extract and format necessary information
            requestedInformation = str(entry["dateTime"]) + SEPARATOR + str(entry["roomID"])
            
            # retrieve image from file system
            requestedImage = self.retrieveImage(entry["image"])
            
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
    