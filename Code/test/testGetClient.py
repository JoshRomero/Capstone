import requests
import json
payload = {
    "objectQueried": "keys"
}
url = "https://objectfinder.tech/pidata"
r = requests.get(url, params=payload)
print(r.text)
