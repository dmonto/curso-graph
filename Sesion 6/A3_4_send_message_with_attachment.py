import requests
import os
from A0_1_get_token import get_delegated_token

def send_message_with_attachment(access_token, team_id, channel_id, message_text, file_url, file_name):
    """Publica un mensaje con archivo adjunto."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "body": {
            "contentType": "html",
            "content": message_text
        },
        "attachments": [
            {
                "id": "1",
                "contentType": "reference",
                "contentUrl": file_url,
                "name": file_name
            }
        ]
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    return response.status_code == 201

# USO
SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
send_message_with_attachment(
    token,
    team_id,
    channel_id,
    "Revisa el presupuesto adjunto",
    "https://sharepoint.com/.../presupuesto.xlsx",
    "Presupuesto 2025"
)