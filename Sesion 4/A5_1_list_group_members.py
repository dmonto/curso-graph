import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GROUP_ID = os.getenv("GROUP_ID")

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

def list_group_members():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Paginación iterativa
    url = "https://graph.microsoft.com/v1.0/groups/{}/members".format(GROUP_ID)
    params = {
        "$select": "id,displayName,userPrincipalName,mail",
        "$top": 20,
    }
    
    member_count = 0
    while url:
        if member_count == 0:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
        else:
            resp = requests.get(url, headers=headers, timeout=15)
        
        resp.raise_for_status()
        data = resp.json()
        
        for m in data.get("value", []):
            print(f"  {m['id']} | {m['displayName']} | {m.get('userPrincipalName', 'N/A')}")
            member_count += 1
        
        url = data.get("@odata.nextLink")
    
    print(f"\nTotal miembros: {member_count}")

if __name__ == "__main__":
    list_group_members()