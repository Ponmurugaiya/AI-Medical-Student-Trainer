# models/mistral_api.py

import requests
from API_KEYS import my_mistral_api_key

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = "my_mistral_api_key"  # <-- Replace with your actual key

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def call_mistral(messages: list, model="mistral-medium"):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 1024
    }

    response = requests.post(MISTRAL_API_URL, json=payload, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Mistral API Error: {response.status_code}, {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
