import requests
import json
payload = {
    "userID": "testID",
    "objectQueried": "keys"
}
url = "http://18.188.84.183:12001/pidata"
r = requests.get(url, params=payload)
info = json.loads(json.loads(r.text))
print(info['dateTime'][11:13])
print(info['dateTime'][14:16])
