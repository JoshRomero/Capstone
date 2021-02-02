# Clark Foster
# This python program is a server to receive files using TCP


import socket
import tqdm
import os

# this device's IP
SERVER_HOST = "138.47.138.121"
SERVER_PORT = 1337

# receive 4096 bytes each step
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create server socket (TCP) and bind to local address
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

# enable server to accept connections with 5 as # unaccepted connections
# that system will allow before refusing new ones
s.listen(5)
print("Listening as {}:{}".format(SERVER_HOST, SERVER_PORT))

# accept connections
client_socket, address = s.accept()
print("[+] {} is connected.".format(address))

# receive the file indo using client socket not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
#remove absolute path if exist
filename  = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# Now start receiving file from socket and writing to file stream
progress = tqdm.tqdm(range(filesize), "Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # then nothing is received and transmission complete
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update progress bar
        progress.update(len(bytes_read))

#close the client socket
client_socket.close()
#close server socket
s.close()