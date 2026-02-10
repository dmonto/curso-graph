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

def list_users_optimized():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Parámetros OData: solo 3 propiedades, máx 5 usuarios, ordenados por nombre
    params = {
        "$select": "id,displayName,userPrincipalName",
        "$orderby": "displayName",
        "$top": 5,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    for u in resp.json().get("value", []):
        print(u)

if __name__ == "__main__":
    list_users_optimized()