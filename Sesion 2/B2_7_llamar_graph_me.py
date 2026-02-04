import requests
from B2_4_obtener_token_device_code import obtener_token_device_code

def llamar_graph_me(token: str):
    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("Usuario:", data.get("displayName"), "-", data.get("mail"))

if __name__ == "__main__":
    llamar_graph_me(obtener_token_device_code())