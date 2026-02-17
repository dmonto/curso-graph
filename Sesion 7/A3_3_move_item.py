import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def move_item(access_token, drive_id, item_id, new_parent_id):
    """Mueve una carpeta o archivo a otro destino."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "parentReference": {
            "id": new_parent_id
        }
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        item = response.json()
        return {
            "status": "success",
            "name": item.get("name"),
            "path": item.get("parentReference", {}).get("path")
        }
    
    return {"status": "failed"}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
folder_id = os.getenv("FOLDER_ID") or input("Id de Nuevo Folder Padre:")
result = move_item(token, drive_id, item_id, folder_id)
print(f"Movido a: {result['path']}")