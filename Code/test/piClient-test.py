import pyrebase
import requests

email = "johndoe@gmail.com"
password = "Pa55w0rd!"
room = "Bedroom"

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

# payload = {
#     "email": email,
#     "password": password,
#     "roomID": room
# }
# url = "http://192.168.1.39:5000/register"
# r = requests.post(url, json=payload)

url = "https://objectfinder.tech/devices"
r = requests.get(url, headers=header)
print(r.text)

url = "http://192.168.1.39:5000/room"
r = requests.get(url, headers=header)
print(r.text)

payload = {
    "roomID": "Kitchen"
}
r = requests.post(url, json=payload, headers=header)
print(r)

url = "http://192.168.1.39:5000/room"
r = requests.get(url, headers=header)
print(r.text)

url = "http://192.168.1.39:5000/status"
r = requests.get(url, headers=header)
print(r.text)

payload = {
    "status": 'START'
}
r = requests.post(url, json=payload, headers=header)
print(r)

r = requests.get(url, headers=header)
print(r.text)

payload = {
    "status": 'STOP'
}
r = requests.post(url, json=payload, headers=header)
print(r)

r = requests.get(url, headers=header)
print(r.text)

payload = {
    "status": 'RESET'
}
r = requests.post(url, json=payload, headers=header)
print(r)