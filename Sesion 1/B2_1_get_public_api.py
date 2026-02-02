import requests

def get_public_api():
    url = "https://httpbin.org/get"
    params = {"curso": "graph", "nivel": "basico"}

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()  # lanza excepción si status >= 400

    data = resp.json()
    print("URL efectiva:", data["url"])
    print("Headers vistos por el servidor:", data["headers"])

if __name__ == "__main__":
    get_public_api()