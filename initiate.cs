import requests
import json

url = 'http://127.0.0.1:5000/initiate-call'
data = {
    'from_number': '89XXXX1132',
    'to_number': '62XXXXX232'
}
headers = {'Content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.json())
