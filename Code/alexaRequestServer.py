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

class AlexaRequestServer(Server):
    serverPort = 6000
    serverIP = socket.gethostbyname(socket.gethostname())

    def __init__(self):
        super().__init__(AlexaRequestServer.serverIP, AlexaRequestServer.serverPort)
        self.database = self.authenticateToDatabase('serverNode', '7$dsV!G3D0Oc')

    # process run by each thread
    def run(self, connectionSocket, ipAddress):
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

        if entry != None:
            # extract and format necessary information
            requestedInformation = "Your {} was found in room {} at {}".format(incomingRequest, str(entry["roomID"]), str(entry["dateTime"]))
        else:
            requestedInformation = "Sorry, your object could not be found"

        # encode and send necessary info
        encodedInformation = requestedInformation.encode()
        connectionSocket.send(encodedInformation)
            
        connectionSocket.close()

    def listenForUsers(self):
        self.sock.listen(100)
        while True:
            clientConnectionSocket, clientAddress = self.sock.accept()
            clientConnectionSocket.settimeout(60)
            print("[+] User connected from {}".format(clientAddress))
            Thread(target = self.run, args = (clientConnectionSocket, clientAddress)).start()

if __name__ == "__main__":
    alexaRequestServer = AlexaRequestServer()
    alexaRequestServer.listenForUsers()