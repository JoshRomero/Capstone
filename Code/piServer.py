import socket
from threading import Thread
from serverTemplate import Server
import json
import os

# NEED TO ADD TOKENS,
# INPUT VALIDATION

class PiServer(Server):
    serverPort = 24002
    serverIP = socket.gethostbyname(socket.gethostname())

    def __init__(self):
        super().__init__(PiServer.serverIP, PiServer.serverPort)
        self.database = self.authenticateToDatabase('rPiCamNode', 'G7q1D^3Bh3Ql')
    
    # def verifyMessage(self, msg):
    #     pass
    
    # saves image to file system and adds image path to entry
    def saveImage(self, imgBytes, uid, entry):
        userPath = "./userImgs/{}".format(uid)
        if os.path.isdir(userPath) == False:
            os.mkdir(userPath)
            
        imgPath = "./userImgs/{}/{}_{}.jpg".format(uid, entry["roomID"], entry["dateTime"])
        
        with open(imgPath, "wb+") as capturedImage:
            capturedImage.write(imgBytes)
        
        entry["image"] = imgPath
    
    def run(self, connectionSocket):
        while True:
            # receive token
            
            # verify token
            uid = "testID" # temporary, needs to be replaced by token
            
            # verify message
            
            # receive entry and decode use decode() + loads() to convert to dictionary
            entryBytes = self.recvMessage(connectionSocket)
            entry = json.loads(entryBytes.decode('utf-8'))
            
            # receive image and save to file system under user's folder
            imageBytes = self.recvMessage(connectionSocket)
            self.saveImage(imageBytes, uid, entry)
            
            # send entry to database
            self.database.camNodeResults.insert_one(entry)
            
            print("Entry inserted into database!")
    
    def listenForPis(self):
        self.sock.listen(100)
        while True:
            clientConnectionSocket, clientAddress = self.sock.accept()
            clientConnectionSocket.settimeout(60)
            print("[+] Pi connected from {}".format(clientAddress))
            
            sslConnection = self.sslContext.wrap_socket(clientConnectionSocket, server_side=True)
            print("SSL established. Peer: {}".format(sslConnection.getpeercert()))
            
            Thread(target = self.run, args = (sslConnection,)).start()

if __name__ == "__main__":
    piServer = PiServer()
    piServer.listenForPis()