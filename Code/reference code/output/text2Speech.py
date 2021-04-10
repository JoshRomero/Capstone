import pyttsx3
from gtts import gTTS
import os
from playsound import playsound
import tempfile


def speechOutput(requestedItem, roomID, dateTime):
    with tempfile.NamedTemporaryFile(suffix = ".mp3") as tmpSpeech:
        text = ("I have found your " + requestedItem + " in room " + roomID + " at " + dateTime)
        language = "en"
        speechObject = gTTS(text=text, lang=language, slow=False)
        speechObject.save(tmpSpeech.name) 
    
        playsound(tmpSpeech.name)
        
        tmpSpeech.close()

