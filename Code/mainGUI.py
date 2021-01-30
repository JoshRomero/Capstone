import text
import microphone
from tkinter import *

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
    # checks if textbox is empty
    if textInput1.get() == "" :
        temporary = "Error: Text Field is Empty"
        mainText1.configure(text = temporary)
    else :
        # calls text function
        text.textFunction(textInput1.get())

        # updates mainText1
        temporary = "Text Sent to Server"
        mainText1.configure(text = temporary)


def microphoneFunctionCall():
    
    # calls microphone function
    microphone.microphoneFunction()

    # updates mainText1
    temporary = "Audio Sent to Server"
    mainText1.configure(text = temporary)


# creates text button
textButton = Button(main, text = "Search with Text" , fg = "blue", command=textFunctionCall)
textButton.grid(column=1, row=6)

# creates microphone button
microphoneButton = Button(main, text = "Search with Microphone", fg = "red", command=microphoneFunctionCall)
microphoneButton.grid(column=3, row=6)


# executes main window
main.mainloop()