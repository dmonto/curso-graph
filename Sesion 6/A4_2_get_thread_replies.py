import requests
import os
from A0_1_get_token import get_apponly_token

def get_thread_replies(access_token, team_id, channel_id, message_id, top=100):
    """Obtiene todas las respuestas a un mensaje."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies",
        headers=headers,
        params={
            "$top": top,
            "$orderby": "createdDateTime asc",
            "$select": "id,createdDateTime,from,body,importance"
        },
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        replies = response.json().get("value", [])
        return [
            {
                "id": reply["id"],
                "author": reply.get("from", {}).get("user", {}).get("displayName"),
                "author_id": reply.get("from", {}).get("user", {}).get("id"),
                "content": reply.get("body", {}).get("content", ""),
                "timestamp": reply.get("createdDateTime"),
                "importance": reply.get("importance")
            }
            for reply in replies
        ]
    
    return []

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
message_id = os.getenv("MESSAGE_ID") or input("Id de Mensaje:")
replies = get_thread_replies(token, team_id, channel_id, message_id)
for reply in replies:
    print(f"  → {reply['author']}: {reply['content'][:50]}...")