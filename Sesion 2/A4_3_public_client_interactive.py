import os
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]

def get_token_interactive():
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    # MSAL abrirá el navegador y escuchará en http://localhost
    result = app.acquire_token_interactive(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Error MSAL (interactive): {result.get('error_description')}")
    return result["access_token"]

if __name__ == "__main__":
    token = get_token_interactive()
    print("Token obtenido (len):", len(token))