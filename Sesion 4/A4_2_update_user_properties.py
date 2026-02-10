import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_ID = os.getenv("USER_ID")

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

def update_user_profile():
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Datos a actualizar: solo los cambios
    update_data = {
        "jobTitle": "Ingeniero 10x"
    }
    
    resp = requests.patch(
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}",
        headers=headers,
        json=update_data,
        timeout=15,
    )
    
    print(f"Status: {resp.status_code}")
    if resp.status_code in [200, 204]:
        print("✅ Usuario actualizado exitosamente")
        if resp.status_code == 200:
            print("Propiedades actualizadas:")
            print(resp.json())
    else:
        print("❌ Error al actualizar usuario:")
        try:
            print(resp.json())
        except Exception:
            print(resp.text)

if __name__ == "__main__":
    update_user_profile()