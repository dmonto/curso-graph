import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_folder_children(access_token, drive_id, folder_id=None, top=100):
    """Obtiene los elementos de una carpeta."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Si folder_id es None, usa root
    folder_path = f"/drives/{drive_id}/items/{folder_id}/children" if folder_id else f"/drives/{drive_id}/root/children"
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0{folder_path}",
        headers=headers,
        params={
            "$top": top,
            "$select": "id,name,size,createdDateTime,lastModifiedDateTime,folder,file",
            "$orderby": "name"
        },
        timeout=30
    )
    print(response.json())
    
    if response.status_code == 200:
        items = response.json().get("value", [])
        return [
            {
                "id": item["id"],
                "name": item.get("name"),
                "type": "folder" if "folder" in item else "file",
                "size": item.get("size", 0),
                "children_count": item.get("folder", {}).get("childCount", 0) if "folder" in item else 0,
                "created": item.get("createdDateTime"),
                "modified": item.get("lastModifiedDateTime")
            }
            for item in items
        ]
    
    return []

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
children = get_folder_children(token, drive_id)
for item in children:
    icon = "📁" if item["type"] == "folder" else "📄"
    print(f"{icon} {item['name']} ({item['id']}, {item['size']} bytes)") 