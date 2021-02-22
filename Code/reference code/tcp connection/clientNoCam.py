## Clark Foster
# This file sends a file over python socket using TCP

import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # each step we will send 4096 bytes

# specify the ip and port of server/receiver
host = "138.47.138.121"
port = 1337

# file we want to send and its size
filename = "bro.jpeg"
filesize = os.path.getsize(filename)

# client socket and connect to server
s = socket.socket()
print("[+] Connecting to {host}:{port}") 
s.connect((host, port))
print("[+] Connected.")

# send the file and its size
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# begin sending
progress = tqdm.tqdm(range(filesize), "Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes of the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # transmission complete
            break
        # use sentall to ensure transmission over busy network
        s.sendall(bytes_read)
        # update progress bar
        progress.update(len(bytes_read))

# close socket
s.close()

