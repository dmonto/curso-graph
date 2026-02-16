import json

def enviar_tarjeta_teams(token, team_id, channel_id, titulo, color="Good"):
    """
    Envía una Adaptive Card a un canal de Teams.
    color: Good (Verde), Warning (Amarillo), Attention (Rojo)
    """
    
    # Mapeo de colores semánticos a colores hex de Adaptive Cards
    colors = {
        "Good": "Good",       # Verde
        "Warning": "Warning", # Amarillo
        "Attention": "Attention" # Rojo
    }
    
    # Definición de la Adaptive Card (JSON)
    card_content = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "TextBlock",
                "size": "Medium",
                "weight": "Bolder",
                "text": titulo,
                "color": colors.get(color, "Default")
            },
            {
                "type": "FactSet",
                "facts": [
                    {"title": "Proceso:", "value": "Sincronización Graph"},
                    {"title": "Duración:", "value": "45ms"},
                    {"title": "Errores:", "value": "0"}
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "Ver Logs Completos",
                "url": "https://portal.azure.com"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.4"
    }

    # Payload para Graph API (Message con Attachment)
    payload = {
        "body": {
            "contentType": "html",
            "content": "<attachment id=\"74d20c7f34aa4a7\">" # Referencia al attachment
        },
        "attachments": [
            {
                "id": "74d20c7f34aa4a7",
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": json.dumps(card_content) # El JSON debe ir como string dentro del content si usamos SDK, o directo según endpoint
            }
        ]
    }
    
    # Versión segura para requests estándar:
    payload["attachments"][0]["content"] = card_content 

    endpoint = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 201:
        print("✅ Tarjeta publicada en Teams.")
    else:
        print(f"❌ Error Teams: {response.text}")

# Nota: Requiere permisos ChannelMessage.Send