import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

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

def resolve_group(group_name: str):
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Filtrar grupos por nombre exacto o startsWith
    params = {
        "$filter": f"displayName eq '{group_name}'",
        "$select": "id,displayName,mail,groupTypes",
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/groups",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    groups = resp.json().get("value", [])
    if not groups:
        print(f"No se encontró grupo: {group_name}")
        return None
    
    group = groups[0]
    print(f"✅ Resuelto grupo: {group['displayName']} (ID: {group['id']})")
    return group["id"]

def list_group_members(group_id: str):
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "$select": "id,displayName,userPrincipalName",
        "$top": 10,
    }
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/groups/{group_id}/members",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    print(f"\nMiembros del grupo:")
    for m in resp.json().get("value", []):
        print(f"  {m['id']} | {m['displayName']}")

if __name__ == "__main__":
    group_id = resolve_group("GRUPO FUERTES - EL POZO CURSO")
    if group_id:
        list_group_members(group_id)