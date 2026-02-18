import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def create_anonymous_link(access_token, drive_id, item_id, permission_type="view"):
    """Crea un enlace anónimo (público) de compartición."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "type": "view",  # o "edit"
        "scope": "anonymous"
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/createLink",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    print(response.status_code)
    if response.status_code in [200,201]:
        share = response.json()
        print(share["link"])
        return {
            "status": "success",
            "url": share["link"]["webUrl"],
            "scope": share["link"]["scope"],
            "type": share["link"]["type"],
            "link_id": share["id"]
        }
    
    return {"status": "failed", "error": response.text}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
result = create_anonymous_link(token, drive_id, item_id, "view")
print(f"Enlace público: {result['url']}")