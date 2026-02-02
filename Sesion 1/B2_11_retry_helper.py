import time
import requests

def get_con_reintentos(url, max_retries=3, backoff=2, **kwargs):
    for intento in range(1, max_retries + 1):
        try:
            resp = requests.get(url, timeout=10, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            print(f"Error en intento {intento}: {e}")
            if intento == max_retries:
                raise
            espera = backoff ** intento
            print(f"Reintentando en {espera}s...")
            time.sleep(espera)