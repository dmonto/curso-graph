import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def get_file_versions(access_token, drive_id, item_id):
    """Obtiene el historial de versiones de un archivo."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/versions",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        versions = response.json().get("value", [])
        
        return [
            {
                "version_id": v["id"],
                "size": v.get("size", 0),
                "created": v.get("createdDateTime"),
                "created_by": v.get("createdBy", {}).get("user", {}).get("displayName"),
                "publication": v.get("publication", {}).get("versionId")
            }
            for v in versions
        ]
    
    return []

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
versions = get_file_versions(token, drive_id, item_id)
print(f"Total de versiones: {len(versions)}")
for v in versions:
    print(f"- v{v['publication']}: {v['created']} por {v['created_by']}")