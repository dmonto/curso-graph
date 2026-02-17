import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_parent_folder(access_token, drive_id, item_id):
    """Obtiene la carpeta padre de un elemento."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Primero obtener el item para sacar el parent reference
    item_response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers,
        timeout=30
    )
    
    if item_response.status_code != 200:
        return None
    
    item = item_response.json()
    parent_ref = item.get("parentReference", {})
    parent_id = parent_ref.get("id")
    
    if not parent_id:
        return None  # Es root
    
    # Obtener detalles del parent
    parent_response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_id}",
        headers=headers,
        timeout=30
    )
    print(parent_response.json())
    
    if parent_response.status_code == 200:
        parent = parent_response.json()
        return {
            "id": parent["id"],
            "name": parent.get("name"),
            "path": parent.get("parentReference", {}).get("path", "/"),
            "children_count": parent.get("folder", {}).get("childCount", 0)
        }
    
    return None

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
parent = get_parent_folder(token, drive_id, item_id)
print(f"Padre: {parent['name']}")