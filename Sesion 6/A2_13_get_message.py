import requests
import os
from A0_1_get_token import get_apponly_token

def get_message(access_token, team_id, channel_id, message_id):
    """Obtiene un mensaje específico."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages/{message_id}",
        headers=headers,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        msg = response.json()
        return {
            "id": msg["id"],
            "author": msg.get("from", {}).get("user", {}).get("displayName"),
            "content": msg.get("body", {}).get("content"),
            "timestamp": msg.get("createdDateTime"),
            "edited": msg.get("lastModifiedDateTime"),
            "attachments": msg.get("attachments", []),
            "mentions": msg.get("mentions", [])
        }
    
    return None

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
message_id = input("Id de Mensaje:")
message = get_message(token, team_id, channel_id, message_id)
print(f"Mensaje de {message['author']}: {message['content']}")