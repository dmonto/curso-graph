import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def get_channel_drive_id(access_token, team_id, channel_id):
    """Obtiene el drive ID del canal para acceder a archivos."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener el sitio del equipo
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/filesFolder",
        headers=headers,
        timeout=30
    )
    print(response.json())

    if response.status_code == 200:
        site = response.json()
        site_id = site["parentReference"]
        
        return {
            "status": "success",
            "drive_id": site_id["driveId"],
            "site_id": site_id
        }
    
    return {"status": "failed"}

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
result = get_channel_drive_id(token, team_id, channel_id)
if result["status"] == "success":
    drive_id = result["drive_id"]
    print(f"Drive ID: {drive_id}")