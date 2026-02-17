import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def assign_permission_to_group(access_token, drive_id, item_id, group_email, role="read"):
    """Asigna permiso a un grupo completo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipients": [{"email": group_email}],
        "roles": [role],
        "message": "Grupo con acceso a archivo",
        "sendNotification": True
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/invite",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        return {"status": "success", "group": group_email, "role": role}
    
    return {"status": "failed"}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
result = assign_permission_to_group(token, drive_id, item_id, "CURSO2@cursograph.onmicrosoft.com", "write")