from piServer import PiServer
from iOSRequestServer import RequestServer

if __name__ == "__main__":
    piServer = PiServer()
    piServer.listenForPis()
    
    requestServer = RequestServer()
    requestServer.listenForUsers()