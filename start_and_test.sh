#!/bin/bash
export GOOGLE_GENAI_USE_VERTEXAI=1
export GOOGLE_CLOUD_PROJECT=profitscout-lx6bb
export GOOGLE_CLOUD_LOCATION=global

uv run uvicorn src.main:app --port 8000 &
SERVER_PID=$!
sleep 5

curl -s -X POST "http://localhost:8000/api/screening" \
-H "Content-Type: application/json" \
-d '{"modification_description":"Replace the existing analog main steam line radiation monitors with digital transmitters in Turkey Point Unit 3."}' | jq

kill $SERVER_PID
