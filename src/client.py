
# i need a client.py
# just to send a GET request http to 'http://127.0.0.1:8000/captureAndAnalyze'

import requests

response = requests.get('http://127.0.0.1:8000/captureAndAnalyze')
print(f"Status Code: {response.status_code}")
print("Response Body:")
print(response.text)