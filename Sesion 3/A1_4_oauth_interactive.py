import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]  # permisos delegados

def get_token_interactive():
    # Para Interactive Flow usamos también PublicClientApplication
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )

    # Abre el navegador del sistema para que el usuario inicie sesión y consienta
    result = app.acquire_token_interactive(scopes=SCOPES)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))

    return result["access_token"]

def call_me(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=displayName,mail",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    print(resp.json())

if __name__ == "__main__":
    token = get_token_interactive()
    call_me(token)