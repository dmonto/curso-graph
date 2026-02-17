import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_breadcrumb(access_token, drive_id, item_id):
    """Crea una ruta de navegación desde root hasta el elemento."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    breadcrumb = []
    current_id = item_id
    
    while current_id:
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{current_id}",
            headers=headers,
            timeout=30
        )
        print(response.json())

        if response.status_code != 200:
            break
        
        item = response.json()
        breadcrumb.insert(0, {
            "id": item["id"],
            "name": item.get("name"),
            "type": "folder" if "folder" in item else "file"
        })
        
        # Obtener parent
        parent_id = item.get("parentReference", {}).get("id")
        current_id = parent_id
    
    return breadcrumb

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
breadcrumb = get_breadcrumb(token, drive_id, item_id)
path = " > ".join([item["name"] for item in breadcrumb])
print(f"Ruta: {path}")