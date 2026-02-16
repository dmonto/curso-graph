import requests
import os
from A0_1_get_token import get_delegated_token

def send_message_with_mention(access_token, team_id, channel_id, text, mention_id, mention_name):
    """Publica un mensaje mencionando a un usuario."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Formato especial para menciones
    html_content = f'<at id="0">{mention_name}</at> {text}'
    
    payload = {
        "body": {
            "contentType": "html",
            "content": html_content
        },
        "mentions": [
            {
                "id": 0,
                "mentionText": mention_name,
                "mentioned": {
                    "user": {
                        "id": mention_id,
                        "displayName": mention_name
                    }
                }
            }
        ]
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    return response.status_code == 201

# USO
SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
send_message_with_mention(
    token,
    team_id,
    channel_id,
    "revisa este documento",
    "user_id",
    "Juan Pérez"
)