import requests
import os
from A0_1_get_token import get_apponly_token

def delete_channel(access_token, team_id, channel_id):
    """Elimina un canal del equipo."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}",
        headers=headers,
        timeout=30
    )
    
    return response.status_code == 204

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel a Borrar:")
success = delete_channel(token, team_id, channel_id)