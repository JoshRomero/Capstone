############################################
# Name: Devon Knudsen
# Assignment #2: HTTP over TCP (Client Side)
# Date: 1/10/20
# Written in Python 3.7
############################################

from socket import *
from sys import *

# create client socket
client_socket = socket(AF_INET, SOCK_STREAM)

# define the server ip, port number from command line arguments
server_ip = argv[1]
port_number = argv[2]

# connect to server socket
client_socket.connect((server_ip, int(port_number)))

# define requested file from command line arguemnts
requested_file = argv[3]

# create and print request message
server_request = "GET /{} HTTP/1.1\nHost: {}".format(requested_file, server_ip)
print("HTTP request to server:\n"
      "{}\n".format(server_request))

# send request message back to client
client_socket.send(server_request.encode())

# receive and print response message from server
server_response = client_socket.recv(2048).decode()
print("HTTP response from server:\n"
      "{}".format(server_response))