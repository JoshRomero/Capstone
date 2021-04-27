import requests
import json
import pyrebase
import shutil

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
    "object": "cellphone"
}
url = "https://objectfinder.tech/pidata"
r = requests.get(url, params=payload, headers=header)
print(r.text)
response = json.loads(r.text)

url = "https://objectfinder.tech/pidata/image?dateTime=2021-04-19_21:36:02.088174"
r = requests.get(url, headers=header)
with open("image.jpg", "wb+") as file:
    file.write(r.content)
    file.close()
