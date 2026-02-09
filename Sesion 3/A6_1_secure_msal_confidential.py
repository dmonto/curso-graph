import os
import logging
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

# Logging recomendado: nivel INFO en prod, DEBUG en dev
logging.basicConfig(level=logging.INFO)
logging.getLogger("msal").setLevel(logging.INFO)  # o DEBUG para trazar MSAL

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Configuración opcional
AZURE_REGION = os.getenv("AZURE_REGION")  # p.ej. "westeurope" o dejar vacío
HTTP_TIMEOUT = float(os.getenv("MSAL_HTTP_TIMEOUT", "10"))  # segundos

PROXIES = None
proxy_url = os.getenv("HTTP_PROXY")
if proxy_url:
    PROXIES = {"http": proxy_url, "https": proxy_url}  # formato requests

def get_app_token():
    # MSAL permite pasar proxies y timeout a través de http_client personalizado si lo necesitas.
    # Para scripts sencillos, se puede usar el cliente por defecto e imponer timeout en las llamadas Graph.
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
        azure_region=AZURE_REGION if AZURE_REGION else None,  # opcional
    )
    logging.info("Solicitando token para cliente...")
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        logging.error("Error al obtener token: %s", result.get("error"))
        logging.error("Descripción: %s", result.get("error_description"))
        logging.error("Correlation ID: %s", result.get("correlation_id"))
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def list_users(token: str, top: int = 5):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users"
    params = {"$top": top, "$select": "id,displayName,mail"}
    logging.info("Llamando a Graph /users...")
    resp = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=HTTP_TIMEOUT,   # timeout de red controlado
        proxies=PROXIES,        # uso de proxy si está configurado
    )
    resp.raise_for_status()
    for u in resp.json().get("value", []):
        print(u["id"], "-", u["displayName"], "-", u["mail"])

if __name__ == "__main__":
    token = get_app_token()
    list_users(token)