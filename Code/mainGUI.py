import text
import microphone
import text2Speech
from tkinter import *
import speech_recognition as sr 
import pyttsx3
from socket import *
from base64 import b64decode
import tempfile
from PIL import ImageTk, Image
from time import sleep
import threading

SERVER_DOMAIN = "192.168.1.54"
SERVER_PORT = 12001
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
    
def receiveResponse(sock):

    # receive packet containing the size of the requested info
    dataSize = sock.recv(BUFFER_SIZE).decode()
    dataSize = int(dataSize)

    # receive packets containing the requested info
    bytesReceived = bytearray()
    amountBytesReceived = 0
    while True:
        dataChunk = sock.recv(BUFFER_SIZE)
        bytesReceived.extend(dataChunk)

        amountBytesReceived += len(dataChunk)
        if(amountBytesReceived == dataSize):
            break
    
    # decode and seperate the information
    unencodedResponse = bytesReceived.decode()
    dateTime, roomID, encryptedImageData = unencodedResponse.split(SEPARATOR)
    encryptedImageData =  encryptedImageData.encode("ascii")
    unencryptedImageData = b64decode(encryptedImageData)
    
    return dateTime, roomID, unencryptedImageData

# to possibly replace the last else in text/microphone functions
def findObject(requestedItem):
    
    # connect to server socket
    clientSocket = create_connection((SERVER_DOMAIN, SERVER_PORT))
    
    # send requested object to the server
    clientSocket.sendall(requestedItem.encode())
            
    # receive response from server
    dateTime, roomID, unencryptedImageData = receiveResponse(clientSocket)
    
    with tempfile.NamedTemporaryFile(suffix = ".jpeg") as tmpImage:
        tmpImage.write(unencryptedImageData)
        databaseImage = Image.open(tmpImage.name)

        # resize image for display
        databaseImage = databaseImage.resize((480, 700), Image.ANTIALIAS)
        resizedImage = ImageTk.PhotoImage(databaseImage)

        # display image
        imageBox.configure(image = resizedImage)
        imageBox.image = resizedImage

        tmpImage.close()

    # display text information
    mainText2.configure(text = ("I have found your " + requestedItem + " in room " + roomID + " at " + dateTime))
    
    # open text to speech in another thread
    speechThread = threading.Thread(target=text2Speech.speechOutput, args=(requestedItem, roomID, dateTime))
    speechThread.start()
    speechThread.join()

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
            findObject(temporary)


def microphoneFunctionCall():
    # updates mainText1
    temporary = (microphone.microphoneFunction())
    if temporary == "Invalid input. Try again":
        mainText1.configure(text = temporary)
    else:
        mainText1.configure(text = ("Searching for: " + temporary))
        findObject(temporary)


# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('480x700')
main.configure(background='lightgrey')

# creates the image area for database pic
defaultImage = ImageTk.PhotoImage(Image.open("./images/default.png")) 
imageBox = Label(image = defaultImage)
imageBox.place(x = 250, y = 300, anchor = "center")

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
