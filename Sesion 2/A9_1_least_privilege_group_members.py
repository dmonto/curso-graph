import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Usar .default, pero en la App Registration añadir el permiso mínimo
# sugerido por la referencia para listar miembros de grupo.
SCOPES = ["https://graph.microsoft.com/.default"]

GROUP_ID = os.getenv("GROUP_ID")

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
    url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members?$select=id,displayName,userPrincipalName"
    resp = requests.get(url, headers=headers, timeout=15)
    print("Status:", resp.status_code)
    print(resp.json())

if __name__ == "__main__":
    token = get_app_token()
    list_group_members(token)