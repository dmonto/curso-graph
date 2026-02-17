import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def create_folder(access_token, drive_id, parent_item_id, folder_name):
    """Crea una carpeta en el drive."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": folder_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"  # o "fail", "replace"
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_item_id}/children",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        folder = response.json()
        return {
            "status": "success",
            "id": folder["id"],
            "name": folder.get("name"),
            "path": folder.get("parentReference", {}).get("path")
        }
    
    return {"status": "failed", "error": response.text}

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
    folder_id = os.getenv("FOLDER_ID") or input("Id de Folder Padre:")
    result = create_folder(token, drive_id, folder_id, "Proyectos 2026")
    print(f"Carpeta creada: {result['name']}")