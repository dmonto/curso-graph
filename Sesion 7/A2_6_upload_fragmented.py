import requests
import os
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_apponly_token
from A2_5_create_upload_session import create_upload_session
from dotenv import load_dotenv

load_dotenv()

def upload_fragmented(access_token, drive_id, folder_id, file_path, fragment_size=262144):
    """Sube un archivo grande por fragmentos."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    # 1. Crear sesión
    session_result = create_upload_session(
        access_token,
        drive_id,
        folder_id,
        file_name,
        file_size
    )
    
    if session_result["status"] != "success":
        return session_result
    
    upload_url = session_result["upload_url"]
    
    # 2. Cargar fragmentos
    with open(file_path, 'rb') as f:
        uploaded = 0
        fragment_num = 1
        
        while uploaded < file_size:
            # Leer fragmento
            chunk = f.read(fragment_size)
            chunk_size = len(chunk)
            
            # Calcular rango
            start = uploaded
            end = uploaded + chunk_size - 1
            
            # Headers del fragmento
            fragment_headers = {
                "Content-Length": str(chunk_size),
                "Content-Range": f"bytes {start}-{end}/{file_size}"
            }
            
            # Subir fragmento
            response = requests.put(
                upload_url,
                headers=fragment_headers,
                data=chunk,
                timeout=300
            )
            print(f"Frag {fragment_num}: {response.status_code}")

            if response.status_code in [200, 201]:
                data = response.json()
                # Si devuelve driveItem completo → FIN
                if data.get("id") and data.get("size") == file_size:
                    print("🎉 ¡SUBIDA COMPLETA!")
                    return {
                        "status": "success",
                        "file_id": data["id"],
                        "file_name": data["name"],
                        "webUrl": data.get("webUrl"),
                        "size": data["size"]
                    }
                print(f"Fragmento {fragment_num}: {start}-{end} ✓")
                uploaded += chunk_size
                fragment_num += 1
            else:
                return {
                    "status": "failed",
                    "error": f"Error en fragmento {fragment_num}",
                    "response": response.text
                }
    
    # 3. Completar carga
    print("🔄 Completando sesión...")
    final_headers = {
        "Content-Length": "0",
        "Content-Range": f"bytes */{file_size}"
    }
    final_resp = requests.put(upload_url, headers=final_headers, timeout=60)
    
    print(f"Final: {final_resp.status_code}")
    print(f"Final: {final_resp.json()}")
    
    if final_resp.status_code in [200, 201]:
        data = final_resp.json()
        return {
            "status": "success",
            "file_id": data["id"],
            "file_name": data["name"],
            "size": data["size"],
            "webUrl": data.get("webUrl")
        }
    
    return {"status": "failed", "error": "No completado"}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
folder_id = os.getenv("FOLDER_ID") or input("Id de Folder:")
result = upload_fragmented(
    token,
    drive_id,
    folder_id,
    "Sesion 5.zip",
    fragment_size=1024*1024  # 1 MB
)

print(f"Cargado: {result['file_name']}")