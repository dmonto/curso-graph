import os
import requests
from msal import ConfidentialClientApplication
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TARGET_APP_ID = os.getenv("CLIENT_ID_DELEGATED")  # appId de la app a monitorizar

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

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

def check_secrets_expiry(days_threshold: int = 30):
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Filtrar por appId
    url = f"https://graph.microsoft.com/v1.0/applications?$filter=appId eq '{TARGET_APP_ID}'"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    apps = resp.json().get("value", [])
    if not apps:
        raise RuntimeError("App no encontrada")

    app_obj = apps[0]
    secrets = app_obj.get("passwordCredentials", [])
    now = datetime.now(timezone.utc)

    for s in secrets:
        end = datetime.fromisoformat(s["endDateTime"].replace("Z", "+00:00"))
        days_left = (end - now).days
        print(f"Secret '{s['displayName']}' expira en {days_left} días (end={end.isoformat()})")
        if days_left <= days_threshold:
            print("  ⚠️ ROTAR este secreto pronto")

if __name__ == "__main__":
    check_secrets_expiry(days_threshold=30)