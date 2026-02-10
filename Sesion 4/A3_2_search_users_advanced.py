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

def search_users_by_name(name_fragment: str):
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ConsistencyLevel": "eventual",  # Requerido para búsquedas avanzadas
    }
    
    # Usar $search con tokenización
    params = {
        "$search": f'"displayName:{name_fragment}"',  # comillas para $search
        "$count": "true",
        "$select": "id,displayName,userPrincipalName,mail",
        "$top": 10,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    data = resp.json()
    print(f"Total encontrados (aprox): {data.get('@odata.count', 'N/A')}")
    print(f"Resultados en esta página: {len(data.get('value', []))}\n")
    
    for u in data.get("value", []):
        print(f"  {u['id']} | {u['displayName']} | {u['userPrincipalName']}")

if __name__ == "__main__":
    search_users_by_name("Juan")