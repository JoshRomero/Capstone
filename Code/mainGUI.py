from tkinter import *
import speech_recognition as sr 
import pyttsx3
from socket import *
from base64 import b64decode
import tempfile
from PIL import ImageTk, Image
from gtts import gTTS
from playsound import playsound
from datetime import datetime

SERVER_DOMAIN = "192.168.1.54"
SERVER_PORT = 12001
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
DEBUG = False
    
def validateTextInput(user_input):
    if(DEBUG):
        print("text function executed")
        print("The item you're looking for: " + user_input)

    # Boolean to make sure the user provides correct input
    invalid_input = True

    while(invalid_input):
        
        # if the object is found then store it in a variable and negate the boolean
        if ("thermos" in user_input):
            user_object = "Thermos"
            invalid_input = False
            return user_object
        elif ("keys" in user_input):
            user_object = "Keys"
            invalid_input = False
            return user_object
        elif ("cellphone" in user_input):
            user_object = "Cellphone"
            invalid_input = False
            return user_object
        elif ("wallet" in user_input):
            user_object = "Wallet"
            invalid_input = False
            return user_object
        # if invalid input, tell them to try again but don't negate the boolean
        else:
            return "Invalid input. Try again"

def validateSpeechInput():
    
    # Initialize the recognizer  
    r = sr.Recognizer()  
    
    flag = True
    while(flag):     
    
    # Exception handling to handle 
    # exceptions at the runtime 
        try: 
            
            # use the microphone as source for input. 
            with sr.Microphone() as source2: 
                
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                
                #listens for the user's input  
                audio2 = r.listen(source2) 
                
                # Using ggogle to recognize audio 
                MyText = r.recognize_google(audio2) 
                MyText = MyText.lower()
                
                 
                if(DEBUG):
                    print("You said: "+MyText)
                
                # Splits text input into a list of each word 
                TextList = MyText.split()

                # if the object is found then store it in a variable and negate the boolean
                if ("thermos" in TextList):
                    user_object = "Thermos"
                    flag = False
                    return user_object
                elif ("keys" in TextList):
                    user_object = "Keys"
                    flag = False
                    return user_object
                elif ("phone" in TextList):
                    user_object = "Phone"
                    flag = False
                    return user_object
                elif ("wallet" in TextList):
                    user_object = "Wallet"
                    flag = False
                    return user_object
                # if invalid input, tell them to try again but don't negate the boolean
                else:
                    return "Invalid input. Try again"
            
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
            
        except sr.UnknownValueError: 
            print("unknown error occured") 
            
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

def resizeImage(img):
    
    # resize image for display
    img = img.resize((int(1920/4.5), int(1080/4.5)), Image.ANTIALIAS)
    resizedImg = ImageTk.PhotoImage(img)
    
    return resizedImg
    

def speechOutput(requestedItem, roomID, dateTime):
    with tempfile.NamedTemporaryFile(suffix = ".mp3") as tmpSpeech:
        text = ("I have found your " + requestedItem + " in room " + roomID + " at " + dateTime)
        language = "en"
        speechObject = gTTS(text=text, lang=language, slow=False)
        speechObject.save(tmpSpeech.name) 
    
        playsound(tmpSpeech.name)
        
        tmpSpeech.close()

# to possibly replace the last else in text/microphone functions
def findObject(requestedItem):
    
    # connect to server socket
    clientSocket = create_connection((SERVER_DOMAIN, SERVER_PORT))
    
    # send requested object to the server
    clientSocket.sendall(requestedItem.encode())
            
    # receive response from server
    dateTime, roomID, unencryptedImageData = receiveResponse(clientSocket)
    
    # close client socket after receiving all data from server
    clientSocket.close()
    
    with tempfile.NamedTemporaryFile(suffix = ".jpg") as tmpImage:
        tmpImage.write(unencryptedImageData)
        databaseImage = Image.open(tmpImage.name)

        resizedImage  = resizeImage(databaseImage)
        
        # display image
        imageBox.configure(image = resizedImage)
        imageBox.image = resizedImage

        tmpImage.close()
        
    # format datetime
    dateTime = datetime.strptime(dateTime, '%m-%d-%Y %I:%M:%S %p')

    # display text information
    mainText2.configure(text = ("I have found your " + requestedItem + " in room " + roomID + " at " + dateTime))
    
    # update main window with image before speech
    main.update()
    
    # open text to speech in another thread
    speechOutput(requestedItem, roomID, dateTime)
            
def textFunctionCall():
    # calls text function
    if textInput1.get() == "":
        temporary = "Text Input is Empty"
        mainText1.configure(text = temporary)
    else: 
        temporary = (validateTextInput(textInput1.get().lower()))
        if temporary == "Invalid input. Try again":
            mainText1.configure(text = temporary)
        else:
            mainText1.configure(text = ("Searching for: " + temporary))
            findObject(temporary.lower())

def microphoneFunctionCall():
    # updates mainText1
    temporary = (validateSpeechInput())
    if temporary == "Invalid input. Try again":
        mainText1.configure(text = temporary)
    else:
        mainText1.configure(text = ("Searching for: " + temporary))
        findObject(temporary.lower())

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('480x700')
main.configure(background='lightgrey')

# creates the image area for database pic
defaultImage = Image.open("./images/default.png")
resizedDefaultImage = resizeImage(defaultImage)
imageBox = Label(image = resizedDefaultImage)
imageBox.place(x = 240, y = 410, anchor = "center")

# creates mainText label
mainText = Label(main, text = "Use the Text/Audio Options Below", padx = 5, font = ("Nunito Sans", 9, "bold"))
mainText.place(x = 145, y = 20)
mainText.configure(background='lightgrey')

# creates mainText0 label
mainText0 = Label(main, text = "to Search for your Object.", padx = 5, font = ("Nunito Sans", 9, "bold"), width=27)
mainText0.place(x = 135, y = 40)
mainText0.configure(background='lightgrey')

# creates text entry bot
textInput1 = Entry(main, width=15)
textInput1.place(x = 70, y = 100) 

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
