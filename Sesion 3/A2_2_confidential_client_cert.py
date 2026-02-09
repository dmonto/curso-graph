import os
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Rutas y datos del certificado (ejemplo conceptual)
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")      # PEM de la clave privada
PUBLIC_CERT_PATH = os.getenv("PUBLIC_CERT_PATH")      # PEM del certificado público
THUMBPRINT = os.getenv("CERT_THUMBPRINT")             # thumbprint del cert registrado en la App

def load_cert_credential():
    with open(PRIVATE_KEY_PATH, "r", encoding="utf-8") as f:
        private_key = f.read()
    with open(PUBLIC_CERT_PATH, "r", encoding="utf-8") as f:
        public_cert = f.read()
    return {
        "private_key": private_key,
        "thumbprint": THUMBPRINT,
        "public_certificate": public_cert,
    }

def get_app_token_cert():
    cred = load_cert_credential()
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=cred,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"Error MSAL (cert): {result.get('error_description')}")
    return result["access_token"]

if __name__ == "__main__":
    token = get_app_token_cert()
    print("Token (primeros 50 chars):", token[:50], "...")