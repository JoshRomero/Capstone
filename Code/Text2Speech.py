import pyttsx3

def speechOutput(requestedItem, roomID, dateTime):
    # object creations
    speech = pyttsx3.init()

    # sets speaking rate
    speech.setProperty('rate', 120)

    # sets volume
    speech.setProperty('volume',1.0)

    # sets voice to female
    voices = speech.getProperty('voices')
    speech.setProperty('voice', voices[1].id)
    
    # possible option to save voice to mp3
    # speech.save_to_file('Audio Ouput', 'test.mp3')

    # output speech
    speech.say("I have found your " + requestedItem + " in room " + roomID + " at " + dateTime)
    speech.runAndWait()


# test Variables
requestedItem = "wallet"
roomID = "3"
dateTime = "01:00, December 23, 2021"


# test Function Call
# speechOutput(requestedItem, roomID, dateTime)


