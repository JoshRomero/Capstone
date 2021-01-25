import text
import microphone
from tkinter import *

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('500x300')

# creates mainText1
mainText1 = Label(main, text = "What would you like to search for?")
mainText1.pack()

# creates text entry bot
textInput1 = Entry(main, width=10)
textInput1.pack() 



def textFunctionCall():
    # updates mainText1
    temporary = "Text Function Called"
    mainText1.configure(text = temporary)

    # calls text function
    text.textFunction(textInput1.get())


def microphoneFunctionCall():
    # updates mainText1
    temporary = "Microphone Function Called"
    mainText1.configure(text = temporary)
 
    # calls microphone function
    microphone.microphoneFunction()



# creates text button
textButton = Button(main, text = "Search with Text" , fg = "blue", command=textFunctionCall)
textButton.pack()

# creates microphone button
microphoneButton = Button(main, text = "Search with Microphone", fg = "red", command=microphoneFunctionCall)
microphoneButton.pack()



# executes main window
main.mainloop()