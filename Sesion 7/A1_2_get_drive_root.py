import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_drive_root(access_token, drive_id):
    """Obtiene la carpeta raíz del drive."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root",
        headers=headers,
        params={"$select": "id,name,parentReference,children,fileSystemInfo"},
        timeout=30
    )
    print(response.json())
    
    if response.status_code == 200:
        root = response.json()
        return {
            "id": root["id"],
            "name": root.get("name"),
            "type": "folder",
            "children_count": root.get("folder", {}).get("childCount", 0),
            "path": root.get("parentReference", {}).get("path", "/"),
            "created": root.get("createdDateTime"),
            "modified": root.get("lastModifiedDateTime")
        }
    
    return None

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
root = get_drive_root(token, drive_id)
print(f"Raíz: {root['name']}")
print(f"Elementos: {root['children_count']}")