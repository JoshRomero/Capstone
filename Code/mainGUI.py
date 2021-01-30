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


# Initialize the recognizer  
r = sr.Recognizer()  
  
# Function to convert text to 
# speech 
def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait()

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
    
                print("Did you say "+MyText)
                # Splits text input into a list of each word 
                TextList = MyText.split()
                return TextList
                flag = False
                
                
                
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
            
        except sr.UnknownValueError: 
            print("unknown error occured") 


# creates text button
textButton = Button(main, text = "Search with Text" , fg = "blue", command=textFunctionCall)
textButton.grid(column=1, row=6)

# creates microphone button
microphoneButton = Button(main, text = "Search with Microphone", fg = "red", command=microphoneFunctionCall)
microphoneButton.grid(column=3, row=6)


# executes main window
main.mainloop()