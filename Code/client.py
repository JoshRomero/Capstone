## Clark Foster
# This file sends a file over python socket using TCP

import socket
import os
from time import sleep
from picamera import PiCamera

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # each step we will send 4096 bytes

# specify the ip and port of server/receiver
host = "192.168.1.252"
port = 1337

# mongoDB container ip and port
DATABASE_DOMAIN = '172.17.0.2'
DATABASE_PORT = 27017

#camera setup
camera = PiCamera()
#only for my set up, camera was upside down
camera.rotation = 180
# i found the less resolution made it easier to send
camera.resolution = (1024, 768)

# file we want to send and its size
filename = "boy.jpeg"
filesize = os.path.getsize(filename)
i=1
while True:
    # camera needs to get ready
    sleep(.5)
    # take the picture
    camera.capture('/home/pi/Desktop/boy.jpeg')
    # client socket and connect to server
    s = socket.socket()
    print("[+] Connecting to {host}:{port}") 
    s.connect((host, port))
    print("[+] Connected.")

    # send the file and its size
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # begin sending
    with open(filename, "rb") as f:
        while True:
            # read the bytes of the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # transmission complete
                break
            # use sentall to ensure transmission over busy network
            s.sendall(bytes_read)

    # close socket
    s.close()
    i+=1

