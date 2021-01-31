# Clark Foster
# This python program is a server to receive files using TCP


import socket
import os

# this device's IP
SERVER_HOST = "192.168.1.252"
SERVER_PORT = 1337

# mongoDB container ip and port
DATABASE_DOMAIN = '172.17.0.2'
DATABASE_PORT = 27017

# receive 4096 bytes each step
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create server socket (TCP) and bind to local address
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

# enable server to accept connections with 5 as # unaccepted connections
# that system will allow before refusing new ones
s.listen(5)
i = 1
while True:
    try:
        print("Listening as {}:{}".format(SERVER_HOST, SERVER_PORT))

        # accept connections
        client_socket, address = s.accept()
        print("[+] {} is connected.".format(address))

        # receive the file indo using client socket not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        #remove absolute path if exist
        filename  = os.path.basename(filename)
        filename = filename[:-5]
        filename = filename + '_' + str(i) + ".jpeg"
        # convert to integer
        filesize = int(filesize)

        # Now start receiving file from socket and writing to file stream
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # then nothing is received and transmission complete
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)

        #close the client socket
        client_socket.close()
        i+=1
    except UnicodeDecodeError:
        continue
#close server socket
s.close()