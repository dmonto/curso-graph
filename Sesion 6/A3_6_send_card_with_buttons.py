import requests
import json  
import os
from A0_1_get_token import get_delegated_token

def send_card_with_buttons(access_token, team_id, channel_id, title, description, buttons):
    """Envía tarjeta con botones de acción."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Construir botones
    actions = []
    for button in buttons:
        actions.append({
            "type": "Action.OpenUrl",
            "title": button["title"],
            "url": button["url"]
        })
    
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
                "text": description,
                "wrap": True,
                "spacing": "medium"
            }
        ],
        "actions": actions
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
    
    print("DEBUG PAYLOAD:", json.dumps(payload, indent=2))  # ← Verifica estructura
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,  # requests.json maneja serialización
        timeout=30
    )
    print("STATUS:", response.status_code)
    print(response.json())
    return response.status_code == 201

# USO
SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team: ")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel: ")

buttons = [
    {"title": "Ver Detalles", "url": "https://dashboard.com/report/123"},
    {"title": "Descargar", "url": "https://drive.google.com/file/123"},
    {"title": "Compartir", "url": "https://example.com/share"}
]

send_card_with_buttons(
    token, team_id, channel_id,
    "Nuevo Informe Disponible 🚀",
    "Se ha completado el análisis de Q1 con éxito.",
    buttons
)
