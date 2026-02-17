import requests
import os
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def create_upload_session(access_token, drive_id, folder_id, file_name, file_size):
    """Crea una sesión de carga por fragmentos."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "item": {
            "@microsoft.graph.conflictBehavior": "rename",  # o "replace", "fail"
            "name": file_name
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}:/{file_name}:/createUploadSession",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        session = response.json()
        return {
            "status": "success",
            "upload_url": session["uploadUrl"],
            "expiration": session["expirationDateTime"],
            "next_ranges": session.get("nextExpectedRanges", [])
        }
    
    return {"status": "failed", "error": response.text}

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
    folder_id = os.getenv("FOLDER_ID") or input("Id de Folder:")
    session = create_upload_session(
        token,
        drive_id,
        folder_id,
        "Sesion 5.zip",
        1024 * 1024 * 500  # 500 MB
    )

    print(f"URL de carga: {session['upload_url']}")