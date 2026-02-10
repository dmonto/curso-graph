import os
import time
import random
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

class GraphClientWithRetry:
    def __init__(self, base_delay: float = 1.0, max_delay: float = 30.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.app = ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=AUTHORITY,
        )
    
    def get_token(self) -> str:
        result = self.app.acquire_token_for_client(scopes=SCOPES)
        if "access_token" not in result:
            raise RuntimeError(result.get("error_description"))
        return result["access_token"]
    
    def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        json: dict = None,
        params: dict = None,
        max_retries: int = 4,
    ) -> requests.Response:
        """Petición HTTP con reintentos automáticos."""
        headers = headers or {}
        attempt = 0
        
        while attempt <= max_retries:
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                    params=params,
                    timeout=15,
                )
                
                # No reintentar en caso de éxito o error sin sentido de reintento
                if resp.status_code not in [429, 503]:
                    return resp
                
                # Último intento: devolver respuesta aunque sea error
                if attempt == max_retries:
                    return resp
                
                # Calcular delay
                if "Retry-After" in resp.headers:
                    delay = float(resp.headers["Retry-After"])
                else:
                    exponential = self.base_delay * (2 ** attempt)
                    delay = min(exponential, self.max_delay)
                    delay += random.uniform(0, 1.0)
                
                print(f"[{method} {url}] Status {resp.status_code}, reintentando en {delay:.1f}s...")
                time.sleep(delay)
                attempt += 1
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    raise
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                time.sleep(delay + random.uniform(0, 1.0))
                attempt += 1
        
        return resp

if __name__ == "__main__":
    client = GraphClientWithRetry()
    token = client.get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Llamada con reintentos automáticos
    resp = client.request(
        "GET",
        "https://graph.microsoft.com/v1.0/users?$top=20&$select=id,displayName",
        headers=headers,
    )
    
    print(f"Status: {resp.status_code}")
    if resp.ok:
        print(f"Usuarios: {len(resp.json().get('value', []))}")