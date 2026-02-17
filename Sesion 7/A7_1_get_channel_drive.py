import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_channel_drive(access_token, team_id, channel_id):
    """Obtiene el drive asociado a un canal."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener información del canal
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        channel = response.json()
        
        # El drive está en la propiedad webUrl, necesitamos obtener el site
        # Acceder a través del site de SharePoint del equipo
        site_id_response = requests.get(
            f"https://graph.microsoft.com/v1.0/teams/{team_id}",
            headers=headers,
            timeout=30
        )
        
        team = site_id_response.json()
        
        # Obtener el drive del canal a través del site
        drive_response = requests.get(
            f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}",
            headers=headers,
            timeout=30
        )
        
        return {
            "status": "success",
            "channel_id": channel_id,
            "team_id": team_id,
            "channel_name": channel.get("displayName")
        }
    
    return {"status": "failed"}

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
result = get_channel_drive(token, team_id, channel_id)
print(f"Canal: {result['channel_name']}/{result['team_id']}")