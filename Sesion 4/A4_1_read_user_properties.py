import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_ID = os.getenv("USER_ID")  # o UPN

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

def read_user_profile():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Seleccionar propiedades comunes
    params = {
        "$select": (
            "id,displayName,userPrincipalName,mail,jobTitle,department,"
            "mobilePhone,telephone,officeLocation,city,country,state,postalCode,"
            "accountEnabled,userType,createdDateTime"
        ),
    }
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    user = resp.json()
    
    print("Propiedades del usuario:")
    print(f"  Nombre: {user['displayName']}")
    print(f"  UPN: {user['userPrincipalName']}")
    print(f"  Email: {user.get('mail', 'N/A')}")
    print(f"  Puesto: {user.get('jobTitle', 'N/A')}")
    print(f"  Departamento: {user.get('department', 'N/A')}")
    print(f"  Teléfono móvil: {user.get('mobilePhone', 'N/A')}")
    print(f"  Ciudad: {user.get('city', 'N/A')}")
    print(f"  País: {user.get('country', 'N/A')}")
    print(f"  Cuenta activa: {user.get('accountEnabled', 'N/A')}")

if __name__ == "__main__":
    read_user_profile()