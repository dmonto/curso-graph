import os
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from OpenSSL import crypto  # o usar cryptography, según tu stack

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

CERT_PATH = os.getenv("CERT_PATH")      # ruta a .pfx o .pem
CERT_PASSWORD = os.getenv("CERT_PASSWORD")  # opcional, si el cert está protegido

def load_pfx_certificate(path: str, password: str | None):
    with open(path, "rb") as f:
        pfx_data = f.read()
    pfx = crypto.load_pkcs12(pfx_data, password.encode() if password else None)
    private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
    return private_key.decode(), cert.decode()

def get_token_app_cert() -> str:
    private_key, public_cert = load_pfx_certificate(CERT_PATH, CERT_PASSWORD)
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        client_credential={
            "private_key": private_key,
            "thumbprint": None,     # opcional si quieres usar thumbprint
            "public_certificate": public_cert,
        },
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Error obteniendo token (cert): {result.get('error_description')}")
    return result["access_token"]