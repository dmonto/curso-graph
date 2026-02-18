import requests
import os
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def upload_simple(access_token, drive_id, folder_id, file_path):
    """Sube un archivo pequeño (< 4MB) de forma simple."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Validar tamaño
    file_size = os.path.getsize(file_path)
    if file_size > 4 * 1024 * 1024:
        return {"status": "failed", "error": "Archivo > 4MB, usar subida por fragmentos"}
    
    # Leer archivo
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    # Obtener nombre del archivo
    file_name = os.path.basename(file_path)
    
    # Subir
    response = requests.put(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}:/{file_name}:/content",
        headers=headers,
        data=file_content,
        timeout=60
    )
    print(response.json())
    if response.status_code in [201, 200]:
        uploaded_file = response.json()
        return {
            "status": "success",
            "file_id": uploaded_file["id"],
            "file_name": uploaded_file.get("name"),
            "size": uploaded_file.get("size", 0)
        }
    else:
        return {"status": "failed", "error": response.text}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
folder_id = os.getenv("FOLDER_ID") or input("Id de Folder:")
result = upload_simple(token, drive_id, folder_id, "Sesion 6.zip")
print(f"Subido: {result['file_name']}")