import requests

url = 'http://127.0.0.1:5000/call-report'
params = {
    'phone': '97XXX33155',
    'page': 1,
    'per_page': 10
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.json())
