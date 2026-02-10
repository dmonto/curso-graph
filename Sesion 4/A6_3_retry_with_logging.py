import os
import time
import random
import logging
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def call_graph_with_smart_retry(url: str, params: dict = None, max_retries: int = 4):
    """Llamada a Graph con reintentos inteligentes y logging."""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    base_delay = 1.0
    max_delay = 30.0
    attempt = 0
    
    while attempt <= max_retries:
        try:
            logger.info(f"Intento {attempt+1}/{max_retries+1}: GET {url}")
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            
            if resp.status_code == 200:
                logger.info(f"✅ Éxito (200)")
                return resp.json()
            elif resp.status_code in [429, 503]:
                if attempt == max_retries:
                    logger.error(f"❌ Fallo final con {resp.status_code} después de {max_retries+1} intentos")
                    raise RuntimeError(f"API throttled/unavailable after {max_retries+1} attempts")
                
                # Calcular delay
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    delay = float(retry_after)
                    logger.warning(f"⏳ 429/503 con Retry-After={delay}s (respetando servidor)")
                else:
                    exponential = base_delay * (2 ** attempt)
                    delay = min(exponential, max_delay)
                    delay += random.uniform(0, 1.0)
                    logger.warning(f"⏳ 429/503 con exponential backoff={delay:.1f}s")
                
                time.sleep(delay)
                attempt += 1
            else:
                logger.error(f"❌ Error no reintentable {resp.status_code}: {resp.text}")
                resp.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            if attempt == max_retries:
                logger.error(f"❌ Error de red después de {max_retries+1} intentos: {e}")
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(f"⏳ Error de red, reintentando en {delay:.1f}s")
            time.sleep(delay + random.uniform(0, 1.0))
            attempt += 1
    
    return None

if __name__ == "__main__":
    try:
        data = call_graph_with_smart_retry(
            "https://graph.microsoft.com/v1.0/users",
            params={"$top": 10, "$select": "id,displayName"},
        )
        print("Resultado:", data)
    except Exception as e:
        logger.error(f"Fallo final: {e}")