import requests
import os
from A0_1_get_token import get_delegated_token

def reply_to_message(access_token, team_id, channel_id, message_id, reply_text):
    """Responde a un mensaje específico."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "body": {
            "contentType": "text",
            "content": reply_text
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    return response.status_code == 201

# USO
SCOPES=["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
message_id = input("Id de Mensaje:")
success = reply_to_message(
    token,
    team_id,
    channel_id,
    message_id,
    "Gracias por la actualización"
)