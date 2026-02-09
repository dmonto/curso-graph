import time
import random
import requests

MAX_RETRIES = 3
BASE_DELAY = 1.0  # segundos

TRANSIENT_STATUSES = {429, 500, 502, 503, 504}

def call_graph_with_retries(method: str, url: str, headers: dict, **kwargs):
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.request(method, url, headers=headers, timeout=15, **kwargs)
        status = resp.status_code

        if 200 <= status < 300:
            return resp

        # Errores transitorios → backoff exponencial + jitter
        if status in TRANSIENT_STATUSES:
            delay = BASE_DELAY * (2 ** (attempt - 1))
            delay = delay * random.uniform(1, 1.5)
            print(f"Intento {attempt}: status {status}, reintentando en {delay:.1f}s...")
            time.sleep(delay)
            continue

        # Errores permanentes → no reintentar
        print(f"Error permanente {status}: {resp.text}")
        resp.raise_for_status()

    # Si agotamos los reintentos
    resp.raise_for_status()

def example_list_users(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$top=5&$select=id,displayName,mail"
    resp = call_graph_with_retries("GET", url, headers=headers)
    print(resp.json())