import requests
import os
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def download_file(access_token, drive_id, item_id, output_path):
    """Descarga un archivo del drive."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener URL de descarga
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers,
        timeout=30
    )
    print(response.json())

    if response.status_code != 200:
        return {"status": "failed", "error": "No se pudo obtener item"}
    
    item = response.json()
    download_url = item.get("@microsoft.graph.downloadUrl")
    
    if not download_url:
        return {"status": "failed", "error": "URL de descarga no disponible"}
    
    # Descargar archivo
    download_response = requests.get(
        download_url,
        timeout=300  # 5 minutos para descarga
    )
    
    if download_response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(download_response.content)
        
        return {
            "status": "success",
            "file": item.get("name"),
            "size": item.get("size", 0),
            "path": output_path
        }
    
    return {"status": "failed", "error": "Error en descarga"}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
result = download_file(token, drive_id, item_id, "sesion-5.md")
print(f"Descargado: {result['file']}")