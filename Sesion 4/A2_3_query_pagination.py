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

def iterate_all_users(max_pages: int = 3):  # limitar para demo
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    url = "https://graph.microsoft.com/v1.0/users"
    params = {
        "$select": "id,displayName,mail",
        "$top": 10,
    }
    
    page_count = 0
    total_users = 0
    
    while url and page_count < max_pages:
        # Primera llamada con params, luego solo URL (que ya tiene todo)
        if page_count == 0:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
        else:
            resp = requests.get(url, headers=headers, timeout=15)
        
        resp.raise_for_status()
        data = resp.json()
        
        page_count += 1
        users_in_page = len(data.get("value", []))
        total_users += users_in_page
        
        print(f"Página {page_count}: {users_in_page} usuarios")
        for u in data.get("value", []):
            print("  -", u.get("displayName"), u.get("mail"))
        
        # Siguiente página
        url = data.get("@odata.nextLink")  # None si no hay más
    
    print(f"\nTotal recuperados: {total_users} usuarios")

if __name__ == "__main__":
    iterate_all_users()