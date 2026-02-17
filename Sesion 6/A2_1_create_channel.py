import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def create_channel(access_token, team_id, channel_name, channel_description=""):
    """Crea un nuevo canal en un equipo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "displayName": channel_name,
        "description": channel_description,
        "membershipType": "standard"  # o "private"
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    if response.status_code == 201:
        channel = response.json()
        return {
            "id": channel["id"],
            "name": channel["displayName"],
            "status": "created"
        }
    else:
        return {"status": "failed", "error": response.json()}

# USO
token = get_apponly_token()
team_id = "12801113-b209-4db2-bf9a-835822f0f237"
channel = create_channel(
    token,
    team_id,
    channel_name="marketing-16-Feb",
    channel_description="Canal para equipo de marketing"
)

print(f"Canal creado: {channel['name']}")