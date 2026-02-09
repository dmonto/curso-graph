import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("ACCESS_TOKEN")  # pegar token aquí o en .env

def test_me_raw(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers=headers,
        timeout=15,
    )
    print("Status:", resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Define ACCESS_TOKEN en el entorno")
    test_me_raw(TOKEN)