from dotenv import load_dotenv
from msal import PublicClientApplication
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

def get_delegated_token(scopes, refresh_if_needed: bool = True):
    """Obtener token delegado (usuario presente)."""
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    
    # Usar device code flow para interactividad
    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    
    return result["access_token"]