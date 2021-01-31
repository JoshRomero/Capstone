import speech_recognition as sr 
import pyttsx3


# Initialize the recognizer  
r = sr.Recognizer()  
  
# Function to convert text to 
# speech 
def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 


def microphoneFunction():
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
