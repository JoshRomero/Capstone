import pyrebase

config = {
  "apiKey": "AIzaSyDkYMP_ilWmPr5n0Kt_N7odVehYEw6qh64",
  "authDomain": "objectfinder-3d3f3.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

username = "johndoe@gmail.com"
password = "Pa55w0rd!"
user = auth.sign_in_with_email_and_password(username, password)

print(user["localId"])