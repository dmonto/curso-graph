import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Permiso mínimo recomendado para /me
SCOPES = ["User.Read"]  # delegated[web:221][web:520]

def get_token_device_code():
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    result = app.acquire_token_interactive(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def test_me(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail,userPrincipalName",
        headers=headers,
        timeout=15,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except Exception:
        print("Respuesta texto:", resp.text)
        return

    if resp.status_code == 200:
        print("Token válido para /me. Usuario:")
        print(data)
    else:
        print("Error al llamar /me:")
        print(data)

if __name__ == "__main__":
    token = get_token_device_code()
    test_me(token)