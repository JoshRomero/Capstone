import pyrebase
import requests

config = {
  "apiKey": "AIzaSyDkYMP_ilWmPr5n0Kt_N7odVehYEw6qh64",
  "authDomain": "objectfinder-3d3f3.firebaseapp.com",
  "databaseURL": "https://objectfinder-3d3f3-default-rtdb.firebaseio.com",
  "storageBucket": "objectfinder-3d3f3.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

username = "johndoe@gmail.com"
password = "Pa55w0rd!"
user = auth.sign_in_with_email_and_password(username, password)

print(user["idToken"])

r = requests.get("https://objectfinder.tech/pidata", headers = {"Authorization" : user["idToken"]}, params = {"objectQueried": "keys"})
# r = requests.get("https://objectfinder.tech/pidata", params = {"objectQueried": "keys"})
print(r.text)