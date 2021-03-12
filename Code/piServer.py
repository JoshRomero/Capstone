import socket
from threading import Thread
from serverTemplate import Server
from time import sleep
from datetime import datetime
import json
import os

class PiServer(Server):
    serverPort = 24002
    serverIP = socket.gethostbyname(socket.gethostname())

    def __init__(self):
        super().__init__(PiServer.serverIP, PiServer.serverPort)
        self.database = self.authenticateToDatabase('rPiCamNode', 'G7q1D^3Bh3Ql')
    
    def listenForPis(self):
        self.sock.listen(100)
        while True:
            clientConnectionSocket, clientAddress = self.sock.accept()
            clientConnectionSocket.settimeout(60)
            Thread(target = self.run, args = (clientConnectionSocket, clientAddress)).start()
    
    # def verifyMessage(self, msg):
    #     pass
    
    def saveImage(self, imgBytes, uid, entryDateTime):
        userPath = f"./userImgs/{uid}"
        if os.path.isdir(userPath) == False:
            os.mkdir(userPath)
            
        path = f"./userImgs/{uid}/{entryDateTime}.jpg"
        
        with open(path, "wb+") as capturedImage:
            capturedImage.write(imgBytes)
        
        entry[image] = path
        
        return 1
    
    def run(self, connectionSocket, ipAddress):
        while True:
            # verify token
            # verify message
            
            # switch collections
            # collection = self.goToCollection(uid)
            collection = "camNodeResults"
            
            # receive entry and decode use decode() + loads() to convert to dictionary
            entryBytes = self.recvMessage(connectionSocket)
            entry = json.loads(entryBytes.decode('utf-8'))
            
            # receive image and save to file system under user's folder
            imageBytes = self.recvMessage(connectionSocket)
            self.saveImage(imageBytes, uid, entry[dateTime])
            
            # send entry to database
            self.database.collection.insert_one(entry)
            
    
if __name__ == "__main__":
    PiServer().listenForPis()