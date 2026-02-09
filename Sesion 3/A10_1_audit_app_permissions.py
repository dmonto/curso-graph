import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

AUDIT_CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")       
AUDIT_TENANT_ID = os.getenv("TENANT_ID")
AUDIT_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TARGET_APP_ID = os.getenv("CLIENT_ID_APPONLY")           

AUTHORITY = f"https://login.microsoftonline.com/{AUDIT_TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]    # requiere permisos adecuados para leer apps

def get_audit_token():
    app = ConfidentialClientApplication(
        client_id=AUDIT_CLIENT_ID,
        client_credential=AUDIT_CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def show_app_permissions():
    token = get_audit_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/applications?$filter=appId eq '{TARGET_APP_ID}'"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    apps = resp.json().get("value", [])
    if not apps:
        print("App no encontrada")
        return

    app_obj = apps[0]
    print("Display name:", app_obj.get("displayName"))
    print("\nPermisos delegados:")
    for p in app_obj.get("requiredResourceAccess", []):
        print("  Resource:", p.get("resourceAppId"))
        for ra in p.get("resourceAccess", []):
            print("    - id:", ra.get("id"), "type:", ra.get("type"))

if __name__ == "__main__":
    show_app_permissions()