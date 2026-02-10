import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GROUP_ID = os.getenv("GROUP_ID") or input("Id de Grupo:")
USER_ID = os.getenv("USER_ID")  or input("Id de Usuario:")

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

def list_group_members(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members"
    params = {"$select": "id,displayName,userPrincipalName"}
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    print("Miembros del grupo:")
    for m in resp.json().get("value", []):
        print(m["id"], "-", m["displayName"], "-", m.get("userPrincipalName"))

def list_user_memberof(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/memberOf/microsoft.graph.group"
    params = {"$select": "id,displayName", "$orderby": "displayName"}
    # Para algunas operaciones avanzadas se necesita ConsistencyLevel: eventual
    resp = requests.get(
        url,
        headers={**headers, "ConsistencyLevel": "eventual"},
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    print(f"Grupos de los que {USER_ID} es miembro directo:")
    for g in resp.json().get("value", []):
        print(g["id"], "-", g["displayName"])

if __name__ == "__main__":
    token = get_app_token()
    list_group_members(token)
    print("\n---\n")
    list_user_memberof(token)
    