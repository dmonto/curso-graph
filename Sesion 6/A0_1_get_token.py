from msal import ConfidentialClientApplication, PublicClientApplication
import os
from dotenv import load_dotenv

load_dotenv()
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # permisos de aplicación

def get_apponly_token():
    CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Error en autenticación app-only: {result.get('error_description')}")
    return result["access_token"]

def get_delegated_token(scopes, refresh_if_needed: bool = True):
    """Obtener token delegado (usuario presente)."""
    CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    
    # Usar device code flow para interactividad
    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    
    return result["access_token"]