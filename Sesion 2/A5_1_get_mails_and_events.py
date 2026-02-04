import os
from msal import PublicClientApplication
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Read", "Calendars.Read"]  # delegados

def get_token_device_code():
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError("No se pudo iniciar device flow")
    print("Ve a:", flow["verification_uri"])
    print("Código:", flow["user_code"])
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def get_mails_and_events(token: str):
    headers = {"Authorization": f"Bearer {token}"}

    mail_resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages"
        "?$top=5&$select=subject,sentDateTime",
        headers=headers,
        timeout=15,
    )
    mail_resp.raise_for_status()
    mails = mail_resp.json().get("value", [])

    cal_resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/events"
        "?$top=5&$select=subject,start,end",
        headers=headers,
        timeout=15,
    )
    cal_resp.raise_for_status()
    events = cal_resp.json().get("value", [])

    print("Últimos correos:")
    for m in mails:
        print(m["sentDateTime"], "-", m["subject"])
    print("\nPróximos eventos:")
    for e in events:
        print(e["start"]["dateTime"], "-", e["subject"])

if __name__ == "__main__":
    token = get_token_device_code()
    get_mails_and_events(token)