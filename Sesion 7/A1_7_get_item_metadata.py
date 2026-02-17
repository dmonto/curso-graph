import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_item_metadata(access_token, drive_id, item_id):
    """Obtiene metadatos completos de un elemento."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers,
        timeout=30
    )
    print(response.json())
    
    if response.status_code == 200:
        item = response.json()
        return {
            "id": item["id"],
            "name": item.get("name"),
            "type": "folder" if "folder" in item else "file",
            "size": item.get("size", 0),
            "created": item.get("createdDateTime"),
            "modified": item.get("lastModifiedDateTime"),
            "created_by": item.get("createdBy", {}).get("user", {}).get("displayName"),
            "modified_by": item.get("lastModifiedBy", {}).get("user", {}).get("displayName"),
            "mime_type": item.get("file", {}).get("mimeType"),
            "web_url": item.get("webUrl"),
            "path": item.get("parentReference", {}).get("path"),
            "version": item.get("file", {}).get("hashes", {}).get("quickXorHash"),
            "children_count": item.get("folder", {}).get("childCount", 0) if "folder" in item else 0
        }
    
    return None

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
metadata = get_item_metadata(token, drive_id, item_id)
print(f"Nombre: {metadata['name']}")
print(f"Tamaño: {metadata['size']} bytes")
print(f"Modificado por: {metadata['modified_by']}")