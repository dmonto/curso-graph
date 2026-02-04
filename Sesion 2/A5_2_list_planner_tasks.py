import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Tasks.Read"]  # delegados para Planner

def get_token():
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

def list_planner_tasks(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/planner/tasks",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    tasks = resp.json().get("value", [])
    for t in tasks:
        print(t.get("title"), "-", t.get("id"))

if __name__ == "__main__":
    token = get_token()
    list_planner_tasks(token)