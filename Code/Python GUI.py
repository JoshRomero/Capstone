# Code from Geek for Geeks

from tkinter import *

root = Tk()
root.title("Object Finder Application")
root.geometry('500x300')


select = Label(root, text = "What would you like to search for?")
select.pack()

txt = Entry(root, width=10)
txt.pack() 


def clicked():
    res = "Searching for: " + txt.get()
    select.configure(text = res)
 
btn = Button(root, text = "Search" ,
             fg = "red", command=clicked)
btn.pack()



root.mainloop()