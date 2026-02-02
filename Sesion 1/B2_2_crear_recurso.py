import requests

def crear_recurso():
    url = "https://httpbin.org/post"
    payload = {"nombre": "curso-graph", "tipo": "demo"}

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print("La petición tardó demasiado (timeout)")
        return
    except requests.exceptions.HTTPError as e:
        print("Error HTTP:", e, "status:", resp.status_code)
        return

    data = resp.json()
    print("Servidor recibió JSON:", data["json"])

if __name__ == "__main__":
    crear_recurso()