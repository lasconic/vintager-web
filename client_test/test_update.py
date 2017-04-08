import requests

import sys

if len(sys.argv) != 2:
    exit(0)

key = sys.argv[1]

URL = 'http://localhost:8080/symbol'

payload = {'key': key, "label": "label1", "yes": 1}
r = requests.post(URL, params=payload)
print r.text
