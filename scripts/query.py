import requests
import json

API_URL = "https://nuclear-ai-assistant-2lshkth7qq-uc.a.run.app/api/query/"
response = requests.post(API_URL, json={"question": "What is 10 CFR 50.59 applicability for power uprates?"})
print(response.status_code)
print(json.dumps(response.json(), indent=2) if response.status_code == 200 else response.text)
