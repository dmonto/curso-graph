import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def navigate_path(access_token, drive_id, path):
    """Navega a una ruta específica en el drive."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Normalizar path
    path = path.strip("/").strip(":")
    if not path:
        return get_drive_root(access_token, drive_id)
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{path}:",
        headers=headers,
        params={"$select": "id,name,parentReference,folder,file"},
        timeout=30
    )
    print(response.json())
    
    if response.status_code == 200:
        item = response.json()
        return {
            "id": item["id"],
            "name": item.get("name"),
            "type": "folder" if "folder" in item else "file",
            "path": item.get("parentReference", {}).get("path", "/"),
            "exists": True
        }
    elif response.status_code == 404:
        return {"exists": False, "path": path}
    
    return None

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item = navigate_path(token, drive_id, "Documentos/Proyectos/2025")
if item["exists"]:
    print(f"Encontrado: {item['name']}")
else:
    print(f"Ruta no existe: {item['path']}")