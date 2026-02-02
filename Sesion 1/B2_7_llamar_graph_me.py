import requests

def llamar_graph_me(token: str):
    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("Usuario:", data.get("displayName"), "-", data.get("mail"))