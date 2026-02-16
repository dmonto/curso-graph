import requests
import os
from A0_1_get_token import get_apponly_token

def update_channel(access_token, team_id, channel_id, **updates):
    """Actualiza propiedades del canal."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}",
        headers=headers,
        json=updates,
        timeout=30
    )
    
    return response.status_code == 200

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
update_channel(
    token,
    team_id,
    channel_id,
    displayName="Nuevo nombre",
    description="Nueva descripción"
)