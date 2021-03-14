import socket
from pymongo import MongoClient
import struct

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.serverPort = port
        self.databasePort = 27017
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.serverPort))
    
    def authenticateToDatabase(self, user, password):
        mongo_client = MongoClient("mongodb://{}:{}".format(self.host, self.databasePort))
        
        try:
            rPiDatabase = mongo_client.rPiData
            rPiDatabase.authenticate(name = user, password = password)
        except:
            raise Exception('Authentication Failed')
        
        return rPiDatabase
    
    def recvMessage(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvAll(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        
        # Read the message data
        return self.recvAll(sock, msglen)

    def recvAll(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    
    def sendMessage(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)
    
    # need to install firebase sdk to make work
    # using token uids will allow a table per user
    # def verifyToken(self, connectionSocket):
    #     decoded_token = auth.verify_id_token(id_token)
    #     if decoded_token:
    #         uid = decoded_token['uid']
    #     else:
    #         sys.exit(0)
            
    #     return uid