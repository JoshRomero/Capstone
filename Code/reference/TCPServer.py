############################################
# Name: Devon Knudsen
# Assignment #2: HTTP over TCP (Server Side)
# Date: 1/10/20
# Written in Python 3.7
############################################

from socket import *

PORT = 12001

# create server socket and bind to PORT
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', PORT))

# keep socket listening to connections
server_socket.listen(1)
print("Server is ready to receive...\n")

# run forever loop to connect and receive messages
while(True):
      # create connection socket and receive request message from connection socket
      connection_socket, address = server_socket.accept()
      incoming_request = connection_socket.recv(2048).decode()
      
      # print incoming http request
      print("HTTP request:\n"
            "{}\n".format(incoming_request))
      
      # parse request and print name of object to be fetched
      parsed_request = incoming_request.split()
      requested_file = parsed_request[1][1:]
      print("Object to be fetched: {}".format(requested_file))
      
      # if file exists
      try:
            # open requested file
            file = open(requested_file, "r")
            file_contents = file.read()
            
            # print contents of requested file
            print("Object content:\n"
                  "{}\n".format(file_contents))
            
            # create and print response message
            request_status = "200 OK"
            request_response = "HTTP/1.1 {}\n\n{}".format(request_status, file_contents)
            print("HTTP response message:\n"
                  "{}\n".format(request_response))
            
            # send response message back to client
            connection_socket.send(request_response.encode())
      
      # if file does not exist
      except IOError:
            # create and print response message
            request_status = "404 Not Found"
            request_response = "HTTP/1.1 {}".format(request_status)
            print("HTTP response message:\n"
                  "{}\n".format(request_response))
            
            # send response message back to client
            connection_socket.send(request_response.encode())
      
      # close the connection socket
      connection_socket.close()
    
    