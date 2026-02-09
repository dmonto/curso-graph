import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # permisos de aplicación preconsentidos

def get_app_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(
            f"Error MSAL: {result.get('error')} - {result.get('error_description')}"
        )
    return result["access_token"]

def run_job():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users?$top=10&$select=id,displayName,mail",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    users = resp.json().get("value", [])
    for u in users:
        print(u["id"], "-", u["displayName"], "-", u["mail"])

if __name__ == "__main__":
    run_job()