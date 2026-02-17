import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def share_with_person(access_token, drive_id, item_id, email, permission_type="view"):
    """Comparte un archivo con una persona específica."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipients": [
            {"email": email}
        ],
        "message": f"Se ha compartido un documento contigo",
        "requireSignIn": True,
        "sendInvitation": True,        
        "roles": [permission_type]  # "read" o "write"
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/invite",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        result = response.json()
        return {
            "status": "success",
            "email": email,
            "permission_id": result.get("value", [{}])[0].get("id"),
            "role": permission_type
        }
    
    return {"status": "failed", "error": response.text}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
result = share_with_person(token, drive_id, item_id, "diego.montoliu@cursograph.onmicrosoft.com", "read")