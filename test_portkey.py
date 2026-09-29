import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
api_key = os.getenv("PORTKEY_API_KEY")
url = "https://api.portkey.ai/v1/chat/completions"

def test_headers(headers, payload):
    headers["x-portkey-api-key"] = api_key
    headers["Content-Type"] = "application/json"
    r = requests.post(url, headers=headers, json=payload)
    print(f"Headers: {headers.get('x-portkey-provider', '')} | {headers.get('x-portkey-virtual-key', '')} | {headers.get('x-portkey-config', '')}")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}\n")

payload = {
    "messages": [{"role": "user", "content": "hello"}],
    "model": "openai/gpt-oss-120b"
}

print("Test 1: provider=openai")
test_headers({"x-portkey-provider": "openai"}, payload)

print("Test 2: provider=rag")
test_headers({"x-portkey-provider": "rag"}, payload)

print("Test 3: provider=@rag")
test_headers({"x-portkey-provider": "@rag"}, payload)

print("Test 4: virtual-key=rag")
test_headers({"x-portkey-virtual-key": "rag"}, payload)

print("Test 5: config=rag")
test_headers({"x-portkey-config": "rag"}, payload)

print("Test 6: provider=groq")
test_headers({"x-portkey-provider": "groq"}, payload)
