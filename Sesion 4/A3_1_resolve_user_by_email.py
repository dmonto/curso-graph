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

def resolve_user_by_email(email: str):
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buscar por UPN o email primario, o en proxyAddresses
    filter_query = (
        f"userPrincipalName eq '{email}' "
        f"or mail eq '{email}' "
        f"or proxyAddresses/any(c:c eq 'smtp:{email}')"
    )
    params = {
        "$filter": filter_query,
        "$select": "id,displayName,userPrincipalName,mail",
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    users = resp.json().get("value", [])
    if not users:
        print(f"No se encontró usuario con email: {email}")
        return None
    
    if len(users) > 1:
        print(f"Advertencia: encontrados {len(users)} usuarios con email {email}")
    
    user = users[0]
    print(f"✅ Resuelto: {user['displayName']} (ID: {user['id']})")
    return user["id"]

if __name__ == "__main__":
    user_id = resolve_user_by_email("test@cursograph.onmicrosoft.com")
    if user_id:
        print(f"Puedes usar el ID {user_id} para asignaciones posteriores")