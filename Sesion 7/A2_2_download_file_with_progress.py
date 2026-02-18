import requests
import os
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def download_file_with_progress(access_token, drive_id, item_id, output_path):
    """Descarga con indicador de progreso."""
    
    import requests
    from tqdm import tqdm
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener metadatos
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers,
        timeout=30
    )
    
    item = response.json()
    download_url = item.get("@microsoft.graph.downloadUrl")
    file_size = item.get("size", 0)
    
    # Descargar con progreso
    response = requests.get(download_url, stream=True, timeout=300)
    
    with open(output_path, 'wb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=28):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    return {"status": "success", "file": item.get("name")}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
result = download_file_with_progress(token, drive_id, item_id, "sesion-5.md")