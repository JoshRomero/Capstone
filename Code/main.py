from piServer import PiServer
from iOSRequestServer import iOSRequestServer

if __name__ == "__main__":
    piServer = PiServer()
    piServer.listenForPis()