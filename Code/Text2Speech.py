import pyttsx3

requestedItem = "wallet"
roomID = "3"
dateTime = "December 23, 2021"
clockTime = "4:00pm"

#object creations
speech = pyttsx3.init()

#sets speaking rate
speech.setProperty('rate', 130)

#sets volume
speech.setProperty('volume',1.0)

#sets voice to female
voices = speech.getProperty('voices')
speech.setProperty('voice', voices[1].id)

#output speech
speech.say("I have found your " + requestedItem + " in room " + roomID + " on " + dateTime + " at " + clockTime)
speech.runAndWait()
