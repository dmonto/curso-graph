import requests

def call_me_with_token(token: str):
    url = "https://graph.microsoft.com/v1.0/users"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=15)
    print("Status:", resp.status_code)
    print("Body snippet:", resp.text[:200])

if __name__ == "__main__":
    from A1_1_auth_app_secret import get_token_app_secret
    token = get_token_app_secret()
    call_me_with_token(token)