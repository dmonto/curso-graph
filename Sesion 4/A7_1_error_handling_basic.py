import os
import logging
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def safe_graph_call(url: str, method: str = "GET", json_body: dict = None):
    """Llamada a Graph con manejo centralizado de errores."""
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=15)
        elif method == "PATCH":
            resp = requests.patch(url, headers=headers, json=json_body, timeout=15)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=json_body, timeout=15)
        else:
            resp = requests.request(method, url, headers=headers, json=json_body, timeout=15)
        
        # Extraer info de error si la hay
        if not resp.ok:
            error_info = resp.json().get("error", {})
            code = error_info.get("code", "Unknown")
            msg = error_info.get("message", "No message")
            request_id = error_info.get("innerError", {}).get("requestId", "N/A")
            
            logger.error(f"Error Graph [{resp.status_code}] {code}: {msg}")
            logger.error(f"Request ID: {request_id}")
            
            # Acciones específicas por status
            if resp.status_code == 401:
                raise RuntimeError("Token expirado o inválido. Renovar credenciales.")
            elif resp.status_code == 403:
                raise PermissionError(f"Permisos insuficientes: {msg}")
            elif resp.status_code == 404:
                logger.warning(f"Recurso no encontrado: {url}")
                return None
            elif resp.status_code == 400:
                raise ValueError(f"Solicitud inválida: {msg}")
            elif resp.status_code >= 429:
                # No lanzar excepción; devolver respuesta para que el caller maneje retry
                logger.warning(f"Throttling/Server error, el caller debe reintentar")
                return resp
            else:
                resp.raise_for_status()
        
        logger.info(f"✅ {method} {url} → {resp.status_code}")
        return resp
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {e}")
        raise

if __name__ == "__main__":
    try:
        # Caso exitoso
        resp = safe_graph_call("https://graph.microsoft.com/v1.0/users?$top=5&$select=id,displayName")
        if resp and resp.ok:
            print(f"Usuarios: {len(resp.json().get('value', []))}")
    except (PermissionError, ValueError, RuntimeError) as e:
        logger.error(f"Fallo: {e}")