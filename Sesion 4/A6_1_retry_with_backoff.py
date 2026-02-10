import time
import requests
from typing import Optional

def request_with_backoff(
    url: str,
    method: str = "GET",
    headers: dict = None,
    json: dict = None,
    max_retries: int = 4,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> Optional[requests.Response]:
    """
    Realizar una petición HTTP con exponential backoff y jitter.
    
    Reintenta en caso de 429 (throttling) o 503 (servicio no disponible).
    Respeta el encabezado Retry-After si está presente.[web:613][web:617]
    """
    import random
    
    attempt = 0
    while attempt <= max_retries:
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=15)
            elif method == "POST":
                resp = requests.post(url, headers=headers, json=json, timeout=15)
            elif method == "PATCH":
                resp = requests.patch(url, headers=headers, json=json, timeout=15)
            elif method == "DELETE":
                resp = requests.delete(url, headers=headers, timeout=15)
            else:
                resp = requests.request(method, url, headers=headers, json=json, timeout=15)
            
            # Si es éxito o error no reintentable, devolver
            if resp.status_code not in [429, 503]:
                return resp
            
            # Si es último intento, devolver respuesta (aunque sea error)
            if attempt == max_retries:
                return resp
            
            # Calcular delay: respetar Retry-After si existe
            if "Retry-After" in resp.headers:
                delay = float(resp.headers["Retry-After"])
                print(f"[Attempt {attempt+1}] 429/503: Retry-After={delay}s (respetando servidor)")
            else:
                # Exponential backoff + jitter
                exponential = base_delay * (2 ** attempt)
                delay = min(exponential, max_delay)
                jitter = random.uniform(0, 1.0)
                delay += jitter
                print(f"[Attempt {attempt+1}] 429/503: backoff={delay:.1f}s")
            
            time.sleep(delay)
            attempt += 1
            
        except requests.exceptions.RequestException as e:
            print(f"[Attempt {attempt+1}] Error de red: {e}")
            if attempt == max_retries:
                raise
            # Backoff para errores de red también
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, 1.0)
            time.sleep(delay + jitter)
            attempt += 1
    
    return None

if __name__ == "__main__":
    # Ejemplo: llamar a Graph /users
    token = "your_token_here"
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = request_with_backoff(
        "https://graph.microsoft.com/v1.0/users?$top=10",
        method="GET",
        headers=headers,
        max_retries=4,
        base_delay=1.0,
    )
    
    if resp:
        print(f"Status: {resp.status_code}")
        if resp.ok:
            print(resp.json())
    else:
        print("Falló después de reintentos")