import os
from msal import PublicClientApplication
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]  # delegados

def get_delegated_token() -> str:
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError("No se pudo iniciar device flow")

    print("Ve a:", flow["verification_uri"])
    print("Código:", flow["user_code"])

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(f"Error MSAL (delegated): {result.get('error_description')}")
    return result["access_token"]

def get_me_profile(token: str):
    url = "https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    token = get_delegated_token()
    me = get_me_profile(token)
    print("Soy:", me["displayName"], "-", me["mail"])