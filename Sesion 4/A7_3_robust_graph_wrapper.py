import os
import time
import random
import logging
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

class GraphError(Exception):
    """Excepción personalizada para errores de Graph."""
    def __init__(self, status_code: int, error_code: str, message: str, request_id: str = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.request_id = request_id
        super().__init__(f"[{status_code}] {error_code}: {message}")

class RobustGraphClient:
    def __init__(self, max_retries: int = 4, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.app = ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=AUTHORITY,
        )
    
    def get_token(self):
        result = self.app.acquire_token_for_client(scopes=SCOPES)
        if "access_token" not in result:
            raise RuntimeError(result.get("error_description"))
        return result["access_token"]
    
    def request(self, method: str, url: str, json_body: dict = None, params: dict = None):
        """Petición HTTP robusto con manejo de errores y reintentos."""
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.request(
                    method, url, headers=headers, json=json_body, params=params, timeout=15
                )
                
                # Éxito
                if resp.ok:
                    logger.info(f"✅ {method} {url} → {resp.status_code}")
                    return resp
                
                # Extraer info de error
                try:
                    error_body = resp.json()
                    error_info = error_body.get("error", {})
                    error_code = error_info.get("code", "UnknownError")
                    error_msg = error_info.get("message", "Unknown")
                    request_id = error_info.get("innerError", {}).get("requestId")
                except Exception:
                    error_code = "Unknown"
                    error_msg = resp.text
                    request_id = None
                
                # Decisión: reintentar o no
                if resp.status_code == 401:
                    logger.error(f"❌ 401 Unauthorized. Token inválido/expirado.")
                    raise GraphError(401, error_code, error_msg, request_id)
                
                elif resp.status_code == 403:
                    logger.error(f"❌ 403 Forbidden. Permisos insuficientes.")
                    raise GraphError(403, error_code, error_msg, request_id)
                
                elif resp.status_code == 404:
                    logger.error(f"⚠️ 404 Not Found: {error_msg}")
                    raise GraphError(404, error_code, error_msg, request_id)
                
                elif resp.status_code == 400:
                    logger.error(f"❌ 400 Bad Request: {error_msg}")
                    raise GraphError(400, error_code, error_msg, request_id)
                
                elif resp.status_code in [429, 503]:
                    # Reintentable
                    if attempt == self.max_retries:
                        logger.error(f"❌ {resp.status_code} después de {self.max_retries+1} intentos")
                        raise GraphError(resp.status_code, error_code, error_msg, request_id)
                    
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after:
                        delay = float(retry_after)
                        logger.warning(f"⏳ {resp.status_code}: esperando {delay}s (Retry-After)")
                    else:
                        delay = min(self.base_delay * (2 ** attempt), 30)
                        delay += random.uniform(0, 1)
                        logger.warning(f"⏳ {resp.status_code}: esperando {delay:.1f}s (backoff)")
                    
                    time.sleep(delay)
                else:
                    logger.error(f"❌ Error HTTP {resp.status_code}: {error_msg}")
                    raise GraphError(resp.status_code, error_code, error_msg, request_id)
            
            except GraphError:
                raise
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries:
                    logger.error(f"❌ Error de conexión después de {self.max_retries+1} intentos: {e}")
                    raise
                delay = min(self.base_delay * (2 ** attempt), 30)
                logger.warning(f"⏳ Error de conexión, esperando {delay:.1f}s...")
                time.sleep(delay)
        
        return None

if __name__ == "__main__":
    client = RobustGraphClient()
    
    try:
        resp = client.request(
            "GET",
            "https://graph.microsoft.com/v1.0/users",
            params={"$top": 10, "$select": "id,displayName"},
        )
        print(f"Usuarios: {len(resp.json().get('value', []))}")
    except GraphError as e:
        logger.error(f"GraphError: {e} (request_id: {e.request_id})")