import text
import microphone
from tkinter import *
import speech_recognition as sr 
import pyttsx3
from socket import *
from base64 import b64decode
from io import BytesIO

SERVER_DOMAIN = "192.168.1.54"
SERVER_PORT = 12001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
    
def receiveResponse():
    bytesReceived = bytearray()
    dataChunk = clientSocket.recv(BUFFER_SIZE)
    while (dataChunk != None):
        bytesReceived.append(dataChunk)
        dataChunk = clientSocket.recv(BUFFER_SIZE)
    
    # decode and seperate the information
    unencodedResponse = bytesReceived.decode()
    dateTime, roomID, encryptedImageData = unencodedResponse.split(SEPARATOR)
    unencryptedImageData = b64decode(encryptedImageData)
    
    return dateTime, roomID, unencryptedImageData

# to possibly replace the last else in text/microphone functions
def findObject(requestedItem):
    # send requested object to the server
    clientSocket.sendall(requestedItem.encode())
            
    # receive response from server
    dateTime, roomID, unencryptedImageData = receiveResponse()
    
    # display information
    imageMemoryStream = BytesIO(unencryptedImageData)
    display.itemconfig(displayVar, image = imageMemoryStream)
    mainText2.configure(text = ("I have found your " + requestedItem + " in the " + roomID + " at " + dateTime))
    
    # clear in-memory byte stream
    imageMemoryStream.seek(0)
    imageMemoryStream.truncate(0)

def textFunctionCall():
    # calls text function
    if textInput1.get() == "":
        temporary = "Text Input is Empty"
        mainText1.configure(text = temporary)
    else: 
        temporary = (text.textFunction(textInput1.get()))
        if temporary == "Invalid input. Try again":
            mainText1.configure(text = temporary)
        else:
            mainText1.configure(text = ("Searching for: " + temporary))

            # data recieved from server
            objectF = "Wallet"
            roomID = "Living Room"
            timeStamp = "12:00am"

            # image recieved from server     
            display.itemconfig(displayVar, image=databaseImage)
            mainText2.configure(text = ("I have found your " + objectF + " in the " + roomID + " at " + timeStamp))

def microphoneFunctionCall():
    # updates mainText1
    temporary = (microphone.microphoneFunction())
    if temporary == "Invalid input. Try again":
        mainText1.configure(text = temporary)
    else:
        mainText1.configure(text = ("Searching for: " + temporary))
        
        # data recieved from server
        objectF = "Wallet"
        roomID = "Living Room"
        timeStamp = "12:00am"

        # image recieved from server     
        display.itemconfig(displayVar, image=databaseImage)
        mainText2.configure(text = ("I have found your " + objectF + " in the " + roomID + " at " + timeStamp))

# connect to server socket
clientSocket = create_connection((SERVER_DOMAIN, SERVER_PORT))

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('480x700')
main.configure(background='lightgrey')

# creates the image area for database pic (NOT WORKING: I just have two test images at the moment)
display = Canvas(main, width = 300, height = 300)      
display.place(x =80, y = 300)   
defaultImage = PhotoImage(file=r"Code\images\default.png")  
databaseImage = PhotoImage(file=r"Code\images\wallet.png")    
displayVar = display.create_image(20,20, anchor=NW, image=defaultImage)

# creates mainText label
mainText = Label(main, text = "Use the Text/Audio Options Below", padx = 5, font = ("Nunito Sans", 9, "bold"))
mainText.place(x = 135, y = 20)
mainText.configure(background='lightgrey')

# creates mainText0 label
mainText0 = Label(main, text = "to Search for your Object.", padx = 5, font = ("Nunito Sans", 9, "bold"), width=27)
mainText0.place(x = 135, y = 40)
mainText0.configure(background='lightgrey')

# creates text entry bot
textInput1 = Entry(main, width=15)
textInput1.place(x = 85, y = 100) 

# hidden text under buttons
mainText1 = Label(main, text = "", padx = 5, font = ("Nunito Sans", 9, "bold"))
mainText1.place(x = 170, y = 200)
mainText1.configure(background='lightgrey')

# hidden text under picture
mainText2 = Label(main, text = "", padx = 5, font = ("Nunito Sans", 9, "bold"))
mainText2.place(x = 80, y = 615)
mainText2.configure(background='lightgrey')
        
# creates text button
textButton = Button(main, text = "Search with Text", fg = "blue", bg = "white", command=textFunctionCall, padx = 5, pady = 5, font = ("Sans Serif", 10))
textButton.place(x = 80, y = 130)

# creates microphone button
microphoneButton = Button(main, text = "Search with Speech", fg = "red", bg = "white", command=microphoneFunctionCall, padx = 5, pady = 5, font = ("Sans Serif", 10))
microphoneButton.place(x = 280, y = 130)


# executes main window
main.mainloop()