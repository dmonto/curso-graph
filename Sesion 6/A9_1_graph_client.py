import requests
import time
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class GraphClient:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        
        # Configuración de reintentos automáticos para conexiones
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,  # Espera 1s, 2s, 4s...
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def resilient_request(self, method, url, **kwargs):
        """
        Realiza cualquier request a Graph con lógica de recuperación completa.
        """
        max_retries = 5
        retries = 0
        
        while retries < max_retries:
            try:
                response = self.session.request(method, url, headers=self.headers, **kwargs)
                
                # Éxito (2xx)
                if 200 <= response.status_code < 300:
                    return response
                
                # Manejo específico por código de estado
                status_code = response.status_code
                
                if status_code == 401:  # Token expirado
                    print("🔄 Renovando token...")
                    # Aquí integrarías renovación con MSAL
                    # self.refresh_token()
                    raise Exception("Token expirado - Implementar renovación")
                
                elif status_code == 429:  # Throttling
                    retry_after = int(response.headers.get('Retry-After', 10))
                    print(f"⏳ Throttling ({retry_after}s). Reintento {retries+1}/{max_retries}")
                    time.sleep(retry_after)
                
                elif status_code in [500, 502, 503, 504]:  # Server Error
                    wait_time = 2 ** retries  # Backoff exponencial
                    print(f"🌐 Server Error {status_code}. Esperando {wait_time}s...")
                    time.sleep(wait_time)
                
                else:  # 400, 404, 403 - No reintentar
                    print(f"❌ Error permanente {status_code}: {response.text[:200]}")
                    response.raise_for_status()
                
                retries += 1
                
            except requests.exceptions.RequestException as e:
                print(f"🌐 Error de conexión: {e}")
                retries += 1
                time.sleep(2 ** retries)
        
        raise Exception(f"❌ Falló tras {max_retries} intentos en {url}")

# --- EJEMPLOS DE USO ---

client = GraphClient("TU_TOKEN")

# 1. Lista de planes (puede fallar por throttling)
planes = client.resilient_request("GET", "https://graph.microsoft.com/v1.0/me/planner/plans").json()

# 2. Crear bucket (puede fallar por 400 si plan_id inválido)
bucket_payload = {
    "name": "01_Desarrollo",
    "planId": "id-del-plan"
}
client.resilient_request("POST", "https://graph.microsoft.com/v1.0/planner/buckets", json=bucket_payload)

print("✅ Todas las operaciones completadas.")