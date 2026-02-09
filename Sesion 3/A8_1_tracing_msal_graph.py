import os
import uuid
import logging
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.getLogger("msal").setLevel(logging.WARNING)  # reducir ruido interno

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_app_token():
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        logging.error("Error al obtener token: %s", result.get("error"))
        logging.error("Descripción: %s", result.get("error_description"))
        logging.error("MSAL correlation_id: %s", result.get("correlation_id"))  # clave para soporte
        raise RuntimeError(result.get("error_description"))
    logging.info("Token obtenido correctamente.")
    return result["access_token"]

def call_graph_with_trace(token: str, url: str):
    trace_id = str(uuid.uuid4())  # ID de correlación propio
    headers = {
        "Authorization": f"Bearer {token}",
        "client-request-id": trace_id,      # Graph lo devolverá en la respuesta
        "Accept": "application/json",
    }
    logging.info("Llamando a Graph %s client-request-id=%s", url, trace_id)
    resp = requests.get(url, headers=headers, timeout=15)

    # Extraer IDs de respuesta de Graph
    request_id = resp.headers.get("request-id")
    client_request_id = resp.headers.get("client-request-id")

    logging.info(
        "Respuesta Graph status=%s request-id=%s client-request-id=%s",
        resp.status_code,
        request_id,
        client_request_id,
    )

    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}

    if not resp.ok:
        logging.error("Error Graph: %s", data)
        resp.raise_for_status()
    return data

if __name__ == "__main__":
    token = get_app_token()
    data = call_graph_with_trace(
        token,
        "https://graph.microsoft.com/v1.0/users?$top=1&$select=id,displayName,mail",
    )
    print(data)