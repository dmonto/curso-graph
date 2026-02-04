import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Ajusta SCOPES según lo que viste en Modify permissions de Graph Explorer
SCOPES = ["User.Read.All"]  # ejemplo para /users

def get_token_device_code():
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
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def test_endpoint():
    token = get_token_device_code()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$top=1&$select=id,displayName,mail"
    resp = requests.get(url, headers=headers, timeout=15)
    print("Status:", resp.status_code)
    try:
        data = resp.json()
        print("Respuesta JSON:", data)
    except Exception:
        print("Respuesta texto:", resp.text)

if __name__ == "__main__":
    test_endpoint()