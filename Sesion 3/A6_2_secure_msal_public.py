import os
import logging
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.getLogger("msal").setLevel(logging.INFO)

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]
HTTP_TIMEOUT = float(os.getenv("MSAL_HTTP_TIMEOUT", "10"))

def get_token_device_code():
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    logging.info("Esperando autenticación de usuario...")
    result = app.acquire_token_interactive(scopes=SCOPES)
    if "access_token" not in result:
        logging.error("Error en device flow: %s", result.get("error"))
        logging.error("Descripción: %s", result.get("error_description"))
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def call_me(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=displayName,mail",
        headers=headers,
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    print(resp.json())

if __name__ == "__main__":
    token = get_token_device_code()
    call_me(token)