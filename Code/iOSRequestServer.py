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

class iOSRequestServer(Server):
    serverPort = 12001
    serverIP = socket.gethostbyname(socket.gethostname())
    
    def __init__(self):
        super().__init__(iOSRequestServer.serverIP, iOSRequestServer.serverPort)
        self.database = self.authenticateToDatabase('serverNode', '7$dsV!G3D0Oc')
    
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
            uid = "testID" # temp to be replaced 
            
            # receive request from connection socket
            incomingRequest = connectionSocket.recv(1024).decode()
            
            if DEBUG:
                print("Item requested from {}: {} at {}".format(ipAddress, incomingRequest, datetime.now()))
            
            # query database for entry
            collection = self.database.camNodeResults
            entry = self.queryDatabase(incomingRequest, collection, uid)
            
            # extract and format necessary information
            if entry != None:
                requestedInformation = "Your {} was found in room {} at {}".format(incomingRequest, str(entry["roomID"]), str(entry["dateTime"]))
            else:
                requestedInformation = "Sorry, your object could not be found"
            
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
            print("[+] User connected from {}".format(clientAddress))
            Thread(target = self.run, args = (clientConnectionSocket, clientAddress)).start()

if __name__ == "__main__":
    iOSRequestServer = iOSRequestServer()
    iOSRequestServer.listenForUsers()