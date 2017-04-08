import requests
import base64
import json

URL = 'http://vintagerwe.appspot.com/symbol'
inputDir = "results"
inputFile = inputDir + "/database.json"

file = open(inputFile, 'rb')
db = json.load(file)

for s in db:
    print s["algorithm"]
    sDict = dict()
    sDict["name"] = s["name"]
    sDict["algorithm"] = s["algorithm"]
    image_file = open(inputDir + "/" + s["name"], "rb")
    encoded_string = base64.b64encode(image_file.read())
    sDict["image"] = encoded_string
    sDict["labels"] = s["label"]
    content = json.dumps(sDict)
    r = requests.put(URL, data=content)
    print r.text
