import requests
import os
from A0_1_get_token import get_apponly_token

def get_channel_messages(access_token, team_id, channel_id, top=10):
    """Obtiene los últimos mensajes de un canal."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        params={
            "$top": top,
        },
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        messages = response.json().get("value", [])
        return [
            {
                "id": msg["id"],
                "author": (msg.get("from", {}) or {}).get("user", {}).get("displayName"),
                "content": msg.get("body", {}).get("content"),
                "timestamp": msg.get("createdDateTime"),
                "importance": msg.get("importance"),
                "type": msg.get("messageType")
            }
            for msg in messages
        ]
    
    return []

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
messages = get_channel_messages(token, team_id, channel_id, top=20)
for msg in messages:
    print(f"[{msg['timestamp']}/{msg['id']}] {msg['author']}: {msg['content'][:50]}...")