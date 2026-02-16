import requests
import json  # ← AÑADIDO (crucial)
import os
from A0_1_get_token import get_delegated_token

def send_simple_card(access_token, team_id, channel_id, title, subtitle, content):
    """Envía una tarjeta adaptativa simple."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Tarjeta adaptativa
    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": title,
                "weight": "bolder",
                "size": "large"
            },
            {
                "type": "TextBlock",
                "text": subtitle,
                "size": "medium",
                "spacing": "none",
                "color": "accent"
            },
            {
                "type": "TextBlock",
                "text": content,
                "wrap": True,
                "spacing": "medium"
            }
        ]
    }
    
    payload = {
        "body": {
            "contentType": "html",
            "content": '<attachment id="card1"></attachment>'  
        },
        "attachments": [
            {
                "id": "card1",  
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": json.dumps(card)  
            }
        ]
    }
    
    print("DEBUG:", json.dumps(payload, indent=2))  
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    print("STATUS:", response.status_code)
    print(response.json())
    return response.status_code == 201

# USO (mismo)
SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team: ")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel: ")
send_simple_card(
    token, team_id, channel_id,
    "📊 Reporte de Ventas",
    "Q1 2026",  
    "Las ventas superaron expectativas con un crecimiento del 25% 📈"
)
