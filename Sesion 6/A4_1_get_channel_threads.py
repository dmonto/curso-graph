import requests
import os
from A0_1_get_token import get_apponly_token

def get_channel_threads(access_token, team_id, channel_id, top=50):
    """Obtiene mensajes principales (raíces de hilos) del canal."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        params={
            "$top": top,
            "$orderby": "createdDateTime desc",
            "$select": "id,createdDateTime,from,body,replyCount,lastModifiedDateTime"
        },
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        messages = response.json().get("value", [])
        return [
            {
                "id": msg["id"],
                "author": msg.get("from", {}).get("user", {}).get("displayName"),
                "author_id": msg.get("from", {}).get("user", {}).get("id"),
                "content": msg.get("body", {}).get("content", ""),
                "timestamp": msg.get("createdDateTime"),
                "reply_count": msg.get("replyCount", 0),
                "last_modified": msg.get("lastModifiedDateTime")
            }
            for msg in messages
        ]
    
    return []

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
threads = get_channel_threads(token, team_id, channel_id, top=100)
print(f"Total de hilos: {len(threads)}")
for thread in threads:
    print(f"- {thread['author']}: {thread['content'][:50]}... ({thread['reply_count']} respuestas)")