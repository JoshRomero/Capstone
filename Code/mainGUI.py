import text
import microphone
from tkinter import *

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('435x300')

# creates mainText1
mainText1 = Label(main, text = "            Please Select Form of Input")
mainText1.grid(column=2, row=1)

# creates text entry bot
textInput1 = Entry(main, width=10)
textInput1.grid(column=1, row=5) 



def textFunctionCall():
    # updates mainText1
    temporary = "              Text Function Called"
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
textButton.grid(column=1, row=6)

# creates microphone button
microphoneButton = Button(main, text = "Search with Microphone", fg = "red", command=microphoneFunctionCall)
microphoneButton.grid(column=3, row=6)



# executes main window
main.mainloop()