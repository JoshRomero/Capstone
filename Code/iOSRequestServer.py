import socket
from threading import Thread
from serverTemplate import Server
from datetime import datetime
import ssl

# NEED TO ADD TOKENS,
# WAY TO SEND THE USER INFO IF THEIR QUIERED OBJECT ISNT FOUND,
# ADD NEW FEATURES FOR IOS APP LIKE ENDING THREAD WHEN APP IS CLOSED

SEPARATOR = "<SEPARATOR>"
DEBUG = False

class RequestServer(Server):
    serverPort = 12001
    serverIP = socket.gethostbyname(socket.gethostname())
    
    def __init__(self):
        super().__init__(RequestServer.serverIP, RequestServer.serverPort)
        self.database = self.authenticateToDatabase('serverNode', '7$dsV!G3D0Oc')
    
    
    # retrieve the newest entry containing the item the user requested
    def queryDatabase(self, object, collection, uid):
        objectProb = "{}Prob".format(object)
        for entry in collection.find({"$and": [{"userID": uid}, {objectProb:1.0}]}).sort("dateTime", -1):
            newestEntry = entry
            break
        
        # insert query information into collection for dashboard
        collection.insert_one({"objectQueried": object})
        
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
            if DEBUG:
                print("Item requested from {}: {} at {}".format(ipAddress, incomingRequest, datetime.now()))
            
            # query database for entry
            collection = self.database.camNodeResults
            uid = "testID"
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
        
        # ssl connection closing
        # sslConnection.shutdown(socket.SHUT_RDWR)
        # sslConnection.close()
        
        connectionSocket.close()
    
    def listenForUsers(self):
        self.sock.listen(100)
        while True:
            clientConnectionSocket, clientAddress = self.sock.accept()
            clientConnectionSocket.settimeout(60)
            print("[+] User connected from {}".format(clientAddress))
            Thread(target = self.run, args = (clientConnectionSocket, clientAddress)).start()

if __name__ == "__main__":
    requestServer = RequestServer()
    requestServer.listenForUsers()