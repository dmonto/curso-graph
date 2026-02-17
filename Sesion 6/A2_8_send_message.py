import requests
import os
from A0_1_get_token import get_delegated_token

def send_message(access_token, team_id, channel_id, message_text):
    """Publica un mensaje simple en un canal."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "body": {
            "contentType": "text",
            "content": message_text
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    if response.status_code == 201:
        message = response.json()
        return {
            "status": "success",
            "message_id": message["id"],
            "timestamp": message.get("createdDateTime")
        }
    else:
        return {
            "status": "failed",
            "error": response.json()
        }

# USO
SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
result = send_message(
    token,
    team_id,
    channel_id,
    "Prueba de Mensaje del 16-Feb"
)

print(f"Mensaje enviado: {result['message_id']}")