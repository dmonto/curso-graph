import os
from msal import PublicClientApplication
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Scopes delegados que la app solicita
SCOPES = ["User.Read"]  # leer perfil y correo del usuario

def get_delegated_token():
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
        raise RuntimeError(f"Error MSAL: {result.get('error_description')}")
    return result["access_token"]

def get_me_and_mail(token: str):
    headers = {"Authorization": f"Bearer {token}"}

    me_resp = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=displayName,mail",
        headers=headers,
        timeout=15,
    )
    me_resp.raise_for_status()
    me = me_resp.json()

    mail_resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages?$top=5&$select=subject,sentDateTime",
        headers=headers,
        timeout=15,
    )
    mail_resp.raise_for_status()
    mails = mail_resp.json().get("value", [])

    print("Usuario:", me["displayName"], "-", me["mail"])
    print("Últimos correos:")
    for msg in mails:
        print(msg["sentDateTime"], "-", msg["subject"])

if __name__ == "__main__":
    token = get_delegated_token()
    get_me_and_mail(token)