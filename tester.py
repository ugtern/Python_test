import requests
import json

url = 'http://0.0.0.0:8088/'
data = {
    'one': '10',
    'two': '15',
}

# req = requests.post(url, json.dumps(data))
# print(req.text)
#
# req = requests.get(url)
# print(req.text)

# req = requests.get('{}log/'.format(url))
# print(req.text)

url_2 = '{}del/'.format(url)
req = requests.delete(url_2)
print(req.text)
