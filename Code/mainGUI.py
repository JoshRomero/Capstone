import text
import microphone
from tkinter import *

# sets up the main window
main = Tk()
main.title("Object Finder Application")
main.geometry('500x300')

# creates label
select = Label(main, text = "What would you like to search for?")
select.pack()

# creates text
txt = Entry(main, width=10)
txt.pack() 



def textFunctionCall():
    temporary = "Text Function Called"
    select.configure(text = temporary)

    # calls text function
    text.textFunction(txt.get())

def microphoneFunctionCall():
    temporary = "Microphone Function Called"
    select.configure(text = temporary)
 
    # calls microphone function
    microphone.microphoneFunction()



# creates text button
textButton = Button(main, text = "Search with Text" , fg = "blue", command=textFunctionCall)
textButton.pack()

# creates microphone button
microphoneButton = Button(main, text = "Search with Microphone", fg = "red", command=microphoneFunctionCall)
microphoneButton.pack()




main.mainloop()