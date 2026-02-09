import requests

def handle_graph_response(resp: requests.Response):
    status = resp.status_code
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text}

    if status == 401:
        print("401 Unauthorized: revisar token (expirado, inválido o para otro recurso).")
        print(body)
    elif status == 403:
        print("403 Forbidden: probablemente permisos insuficientes / falta de consentimiento.")
        print(body)
    elif status in {429, 503, 504}:
        print("Error transitorio (throttling o servicio): aplicar reintento con backoff.")
        print(body)
    else:
        print(f"Error HTTP {status}:")
        print(body)