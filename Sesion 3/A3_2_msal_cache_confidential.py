import os
import requests
import msal
from msal_extensions import (
    FilePersistence,
    PersistedTokenCache,
)
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

CACHE_FILE = "confidential_cache.bin"

def build_cache():
    persistence = FilePersistence(CACHE_FILE)
    cache = PersistedTokenCache(persistence)
    return cache

def get_app_token():
    cache = build_cache()
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
        token_cache=cache,
    )
    result = app.acquire_token_silent(SCOPES, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def list_users(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users?$top=3&$select=id,displayName,mail",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    print(resp.json())

if __name__ == "__main__":
    token = get_app_token()
    list_users(token)