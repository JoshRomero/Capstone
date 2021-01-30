import text
import microphone
from tkinter import *
import speech_recognition as sr 
import pyttsx3

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('424x300')

# creates mainText label
mainText = Label(main, text = "Use the Text/Audio Options Below")
mainText.grid(column=2, row=1)

# creates mainText0 label
mainText0 = Label(main, text = "to Search for your Object.")
mainText0.grid(column=2, row=2)

# creates text entry bot
textInput1 = Entry(main, width=10)
textInput1.grid(column=1, row=5) 

# creates mainText1 label
mainText1 = Label(main, text = " ")
mainText1.grid(column=2, row=7)


def textFunctionCall():
    # calls text function
    temporary = ("Sent Request for: " + text.textFunction(textInput1.get()))
    mainText1.configure(text = temporary)

def microphoneFunctionCall():
    print("Microphone Listening...")
    # updates mainText1
    temporary = ("Sent Request for: " + microphone.microphoneFunction())
    mainText1.configure(text = temporary)


# creates text button
textButton = Button(main, text = "Search with Text" , fg = "blue", command=textFunctionCall)
textButton.grid(column=1, row=6)

# creates microphone button
microphoneButton = Button(main, text = "Search with Microphone", fg = "red", command=microphoneFunctionCall)
microphoneButton.grid(column=3, row=6)


# executes main window
main.mainloop()