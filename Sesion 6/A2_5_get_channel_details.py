import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_channel_details(access_token, team_id, channel_id):
    """Obtiene detalles de un canal específico."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}",
        headers=headers,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        ch = response.json()
        return {
            "id": ch["id"],
            "name": ch["displayName"],
            "description": ch.get("description"),
            "type": ch.get("membershipType"),
            "url": ch.get("webUrl"),
            "created": ch.get("createdDateTime")
        }
    
    return None

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
details = get_channel_details(token, team_id, channel_id)
print(f"Canal: {details['name']}")
print(f"URL: {details['url']}")