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

def list_direct_memberships():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Membresías directas (solo grupos)
    params = {
        "$select": "id,displayName,mail",
        "$top": 20,
    }
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}/memberOf/microsoft.graph.group",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    print("Pertenencias DIRECTAS a grupos:")
    for g in resp.json().get("value", []):
        print(f"  {g['id']} | {g['displayName']}")

def list_transitive_memberships():
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ConsistencyLevel": "eventual",  # Requerido para transitiveMemberOf[web:609]
    }
    
    # Membresías transitivas (directo e indirecto)
    params = {
        "$select": "id,displayName",
        "$count": "true",
        "$orderby": "displayName",
        "$top": 20,
    }
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}/transitiveMemberOf/microsoft.graph.group",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    
    print(f"\nPertenencias TRANSITIVAS a grupos ({data.get('@odata.count', 'N/A')} total):")
    for g in data.get("value", []):
        print(f"  {g['id']} | {g['displayName']}")

if __name__ == "__main__":
    list_direct_memberships()
    list_transitive_memberships()