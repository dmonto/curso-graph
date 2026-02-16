import requests
import os
from A0_1_get_token import get_apponly_token

def share_channel_with_team(access_token, team_id, channel_id, target_team_id):
    """Comparte un canal con otro equipo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "teamId": target_team_id
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/sharedWithTeams",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    return response.status_code == 201

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel Origen:")
target_team_id = os.getenv("TARGET_TEAM_ID") or input("Id de Team Destino:")
share_channel_with_team(
    token,
    team_id,
    channel_id,
    target_team_id
)