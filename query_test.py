import requests

API_URL = "https://nuclear-eng-ai-assistant-469352939749.us-central1.run.app/api/query/"
data = {"question": "What is the purpose of NEI 96-07?", "session_id": "test_session_1"}
response = requests.post(API_URL, json=data)
print(response.status_code)
print(response.json())
