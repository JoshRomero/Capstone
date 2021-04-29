import pyrebase
import requests

email = "johndoe@gmail.com"
password = "Pa55w0rd!"

config = {
  "apiKey": "AIzaSyDkYMP_ilWmPr5n0Kt_N7odVehYEw6qh64",
  "authDomain": "objectfinder-3d3f3.firebaseapp.com",
  "databaseURL": "https://objectfinder-3d3f3-default-rtdb.firebaseio.com",
  "storageBucket": "objectfinder-3d3f3.appspot.com"
}
firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)
header = {"Authorization": user["idToken"]}

payload = {
    "email": email,
    "password": password
    "roomID": 
}
url = "http://192.168.0.111:5000/register"
r = requests.post(url, json=payload, headers=header)

payload = {
    "roomID": "bedroom"
}
url = "http://192.168.1.39:5000/roomID"
r = requests.post(url, json=payload, headers=header)
print(r.text)

url = "http://192.168.1.39:5000/roomID"
r = requests.get(url, headers=header)
print(r.text)

url = "http://192.168.1.39:5000/status"
r = requests.get(url, headers=header)
print(r.text)

payload = {
    "status": "START"
}
url = "http://192.168.1.39:5000/status"
r = requests.post(url, json=payload, headers=header)
print(r.text)

url = "http://192.168.1.39:5000/status"
r = requests.get(url, headers=header)
print(r.text)