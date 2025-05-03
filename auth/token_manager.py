import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

token_url = "https://live-api.statsbomb.com/v1/token"

client_id = os.getenv("STATSBOMB_CLIENT_ID")
client_secret = os.getenv("STATSBOMB_CLIENT_SECRET")

if not client_id or not client_secret:
    raise EnvironmentError("Missing STATSBOMB_CLIENT_ID or STATSBOMB_CLIENT_SECRET in environment.")

payload = {
    "client_id": client_id,
    "client_secret": client_secret
}

headers = {
    "Content-Type": "application/json"
}

token_response = requests.post(token_url, json=payload, headers=headers)
token_response.raise_for_status()

access_token = token_response.json()["access_token"]
print("Access token fetched successfully:", access_token[:10], "...")