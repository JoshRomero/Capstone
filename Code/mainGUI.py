import text
import microphone
from tkinter import *

import speech_recognition as sr 
import pyttsx3

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('480x300')
main.configure(background='lightgrey')


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


# creates mainText1 label
mainText1 = Label(main, text = "", padx = 5, font = ("Nunito Sans", 9, "bold"))
mainText1.place(x = 170, y = 200)
mainText1.configure(background='lightgrey')



def textFunctionCall():
    # calls text function
    if textInput1.get() == "":
        temporary = "Error: Text Input is Empty"
        mainText1.configure(text = temporary)
    else: 
        temporary = (text.textFunction(textInput1.get()))
        if temporary == "Invalid input. Try again":
            mainText1.configure(text = temporary)
        else:
            mainText1.configure(text = ("Searching for: " + temporary))

def microphoneFunctionCall():
    # updates mainText1
    temporary = ("Searching for: " + microphone.microphoneFunction())
    mainText1.configure(text = temporary)


# creates text button
textButton = Button(main, text = "Search with Text", fg = "blue", bg = "white", command=textFunctionCall, padx = 5, pady = 5, font = ("Sans Serif", 10))
textButton.place(x = 80, y = 130)

# creates microphone button
microphoneButton = Button(main, text = "Search with Speech", fg = "red", bg = "white", command=microphoneFunctionCall, padx = 5, pady = 5, font = ("Sans Serif", 10))
microphoneButton.place(x = 280, y = 130)


# executes main window
main.mainloop()