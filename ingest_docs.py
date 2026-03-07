import requests
import os
import glob

API_URL = "https://nuclear-eng-ai-assistant-469352939749.us-central1.run.app/api/documents/"
docs = glob.glob("data/sample_documents/*.pdf")

for doc in docs:
    print(f"Uploading {doc}...")
    with open(doc, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
        print(response.status_code, response.json())
