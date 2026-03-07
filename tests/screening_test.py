import requests

API_URL = "https://nuclear-eng-ai-assistant-469352939749.us-central1.run.app/api/screening/"
data = {"modification_description": "Updating the Turkey Point plant's fire protection system by replacing old sprinklers with higher capacity sprinklers."}
response = requests.post(API_URL, json=data)
print(response.status_code)
print(response.json())
