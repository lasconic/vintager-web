import requests
import base64
import json

URL = 'http://localhost:8080/symbol'


sDict = dict()
sDict["name"] = "symbol1"
sDict["algorithm"] = "cnn"
sDict["labels"] = [{"name": "stem", "probability": "0.5"}, {"name": "G clef", "probability": "0.75"}]

image_file = open("symbol_test.jpg", "rb")
encoded_string = base64.b64encode(image_file.read())
sDict["image"] = encoded_string

content = json.dumps(sDict)

r = requests.put(URL, data=content)
print r.text
