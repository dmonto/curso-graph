from msal import ConfidentialClientApplication
from urllib.parse import urlencode

from A4_1_web_auth_config import CLIENT_ID_DELEGATED, CLIENT_SECRET, AUTHORITY, REDIRECT_URI, SCOPES

app = ConfidentialClientApplication(
    client_id=CLIENT_ID_DELEGATED,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY,
)

def build_auth_url():
    return app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        # state, nonce, etc. deberían usarse en producción
    )

def exchange_code_for_token(auth_code: str):
    result = app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    if "access_token" not in result:
        raise RuntimeError(f"Error en intercambio de código: {result.get('error_description')}")
    return result["access_token"]

if __name__ == "__main__":
    exchange_code_for_token(build_auth_url())
