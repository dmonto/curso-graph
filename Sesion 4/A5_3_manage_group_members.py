import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GROUP_ID = os.getenv("GROUP_ID")
USER_ID = os.getenv("USER_ID")  # usuario a añadir/quitar

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

def add_member_to_group():
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construir referencia OData
    body = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{USER_ID}"
    }
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members/$ref",
        headers=headers,
        json=body,
        timeout=15,
    )
    
    if resp.status_code == 204:
        print(f"✅ Usuario {USER_ID} añadido al grupo {GROUP_ID}")
    elif resp.status_code == 400:
        print(f"❌ Error 400: Usuario ya es miembro o dato inválido")
        print(resp.json())
    elif resp.status_code == 403:
        print(f"❌ Error 403: Permisos insuficientes (se requiere Group.ReadWrite.All)")
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")

def remove_member_from_group():
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.delete(
        f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members/{USER_ID}/$ref",
        headers=headers,
        timeout=15,
    )
    
    if resp.status_code == 204:
        print(f"✅ Usuario {USER_ID} removido del grupo {GROUP_ID}")
    elif resp.status_code == 404:
        print(f"❌ Error 404: Usuario no encontrado en el grupo")
    elif resp.status_code == 403:
        print(f"❌ Error 403: Permisos insuficientes")
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    print("Añadiendo miembro...")
    add_member_to_group()
    print("\nRemoviendo miembro...")
    remove_member_from_group()