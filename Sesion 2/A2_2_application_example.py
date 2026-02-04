import os
from msal import ConfidentialClientApplication
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # usará permisos de aplicación

def get_app_token() -> str:
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Error MSAL (app): {result.get('error_description')}")
    return result["access_token"]

def list_users(token: str, top: int = 5):
    url = "https://graph.microsoft.com/v1.0/users"
    params = {"$top": top, "$select": "id,displayName,mail"}
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("value", [])

if __name__ == "__main__":
    token = get_app_token()
    users = list_users(token)
    for u in users:
        print(u["id"], "-", u["displayName"], "-", u["mail"])