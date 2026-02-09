import os
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
    try:
        result = app.acquire_token_for_client(scopes=SCOPES)
    except ValueError as ex:
        # Errores de servicio AAD
        print("Error al contactar con AAD:", ex)
        raise

    if "access_token" not in result:
        # Errores de MSAL/AAD representados en result
        print("Error al obtener token:")
        print("  error:", result.get("error"))
        print("  descripcion:", result.get("error_description"))
        print("  correlation_id:", result.get("correlation_id"))
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

if __name__ == "__main__":
    token = get_app_token()
    print("Token OK (longitud):", len(token))