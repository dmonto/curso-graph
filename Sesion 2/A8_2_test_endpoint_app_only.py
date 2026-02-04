import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = ["https://graph.microsoft.com/.default"]  # usará permisos de aplicación

def get_app_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def test_endpoint():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$top=1&$select=id,displayName,mail"
    resp = requests.get(url, headers=headers, timeout=15)
    print("Status:", resp.status_code)
    try:
        data = resp.json()
        print("Respuesta JSON:", data)
    except Exception:
        print("Respuesta texto:", resp.text)

if __name__ == "__main__":
    test_endpoint()