import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Resource implícito: Graph (https://graph.microsoft.com)
SCOPES = ["User.Read", "Mail.Read"]  # scoped dentro del resource Graph

def get_token_device_code():
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    result = app.acquire_token_interactive(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def call_me_and_mail(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    me = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=displayName,mail",
        headers=headers,
        timeout=15,
    ).json()
    mails = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages?$top=5&$select=subject,sentDateTime",
        headers=headers,
        timeout=15,
    ).json()["value"]

    print("Usuario:", me["displayName"], "-", me["mail"])
    print("Últimos correos:")
    for m in mails:
        print(m["sentDateTime"], "-", m["subject"])

if __name__ == "__main__":
    token = get_token_device_code()
    call_me_and_mail(token)