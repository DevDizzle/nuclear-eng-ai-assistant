import requests

API_URL = "https://nuclear-ai-assistant-2lshkth7qq-uc.a.run.app/api/documents/"
response = requests.get(API_URL)
print(response.json())
