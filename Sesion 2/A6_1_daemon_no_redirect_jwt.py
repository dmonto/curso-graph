import os
import base64
import json
from msal import ConfidentialClientApplication, PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

def decode_jwt(token: str) -> dict:
    # Formato JWT: header.payload.signature (base64url)
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token no parece un JWT")
    payload = parts[1] + "=" * (-len(parts[1]) % 4)
    data = base64.urlsafe_b64decode(payload.encode("utf-8"))
    return json.loads(data)

def get_app_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

if __name__ == "__main__":
    token = get_app_token()
    claims = decode_jwt(token)
    print("tid (tenant):", claims.get("tid"))
    print("appId (azp):", claims.get("azp"))
    print("roles:", claims.get("roles"))
    print("scp:", claims.get("scp"))  # en tokens delegated