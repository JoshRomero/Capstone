import socket
from threading import Thread
from serverTemplate import Server
import json
import os

class PiServer(Server):
    serverPort = 24002
    serverIP = socket.gethostbyname(socket.gethostname())

    def __init__(self):
        super().__init__(PiServer.serverIP, PiServer.serverPort)
        self.database = self.authenticateToDatabase('rPiCamNode', 'G7q1D^3Bh3Ql')
    
    # def verifyMessage(self, msg):
    #     pass
    
    def saveImage(self, imgBytes, uid, entryDateTime, entryRoomID):
        userPath = "./userImgs/{}".format(uid)
        if os.path.isdir(userPath) == False:
            os.mkdir(userPath)
            
        imgPath = "./userImgs/{}/{}_{}.jpg".format(uid, entryDateTime, entryRoomID)
        
        with open(imgPath, "wb+") as capturedImage:
            capturedImage.write(imgBytes)
        
        entry["image"] = imgPath
    
    def run(self, connectionSocket, ipAddress):
        while True:
            # receive token
            # verify token
            # verify message
            
            # receive entry and decode use decode() + loads() to convert to dictionary
            entryBytes = self.recvMessage(connectionSocket)
            entry = json.loads(entryBytes.decode('utf-8'))
            
            # receive image and save to file system under user's folder
            imageBytes = self.recvMessage(connectionSocket)
            uid = "testID"
            self.saveImage(imageBytes, uid, entry["dateTime"], entry["roomID"])
            
            # send entry to database
            collection = self.database.self.collection
            collection.insert_one(entry)
            
            break
        
        connectionSocket.close()
    
    def listenForPis(self):
        self.sock.listen(100)
        while True:
            clientConnectionSocket, clientAddress = self.sock.accept()
            clientConnectionSocket.settimeout(60)
            print("[+] Pi connected from {}".format(clientAddress))
            Thread(target = self.run, args = (clientConnectionSocket, clientAddress)).start()