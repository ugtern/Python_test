import requests
import json

url = 'http://localhost:8088/'
data = {
    'one': '10',
    'two': '15',
}

# req = requests.get(url)
# print(req.text)
#
# req = requests.post(url, json.dumps(data))
# print(req.text)

req = requests.get('{}log/'.format(url))
print(req.text)
