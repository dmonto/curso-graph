import requests
import os
from A0_1_get_token import get_apponly_token

def get_channel_members(access_token, team_id, channel_id):
    """Obtiene miembros específicos de un canal."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/members",
        headers=headers,
        params={"$select": "id,displayName,roles"},
        timeout=30
    )
    
    print(response.json())
    if response.status_code == 200:
        return response.json().get("value", [])
    
    return []

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
members = get_channel_members(token, team_id, channel_id)
print(members)