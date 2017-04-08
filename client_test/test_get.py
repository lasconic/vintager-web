import requests

import sys

URL = 'http://localhost:8080/symbol'

if len(sys.argv) != 2:
    r = requests.get(URL)
    print r.text
    exit(0)

key = sys.argv[1]

payload = {'key': key}
#r = requests.get(URL, params=payload)
r = requests.get(URL)
print r.text
