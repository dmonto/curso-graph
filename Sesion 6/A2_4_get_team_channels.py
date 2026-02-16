import requests
import os
from A0_1_get_token import get_apponly_token

def get_team_channels(access_token, team_id):
    """Obtiene todos los canales de un equipo."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels",
        headers=headers,
        params={"$select": "id,displayName,description,membershipType"},
        timeout=30
    )
    
    if response.status_code == 200:
        channels = response.json().get("value", [])
        return [
            {
                "id": ch["id"],
                "name": ch["displayName"],
                "type": ch.get("membershipType"),
                "description": ch.get("description", "")
            }
            for ch in channels
        ]
    
    return []

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channels = get_team_channels(token, team_id)
for channel in channels:
    print(f"- {channel['name']} ({channel['type']}/{channel['id']})")