import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_ID = os.getenv("USER_ID")

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

def read_user_with_manager():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "$select": "id,displayName,jobTitle,department",
        "$expand": "manager($select=id,displayName,jobTitle)",
    }
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    user = resp.json()
    
    print(f"Usuario: {user['displayName']}")
    print(f"  Puesto: {user.get('jobTitle', 'N/A')}")
    print(f"  Departamento: {user.get('department', 'N/A')}")
    
    manager = user.get("manager")
    if manager:
        print(f"  Manager: {manager.get('displayName')} ({manager.get('jobTitle')})")
    else:
        print(f"  Manager: N/A")

if __name__ == "__main__":
    read_user_with_manager()