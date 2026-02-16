import requests
import os
from A0_1_get_token import get_apponly_token

def create_moderated_channel(access_token, team_id, channel_name):
    """Crea canal con configuración de moderación."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "displayName": channel_name,
        "description": "Canal moderado",
        "membershipType": "standard",
        "moderationSettings": {
            "userNewMessageRestriction": "everyone",  # Quién puede postear
            "replyRestriction": "everyone",           # Quién puede responder
            "allowUserEditMessages": True,             # Permitir editar
            "allowUserDeleteMessages": True            # Permitir eliminar
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    return response.status_code == 201

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
create_moderated_channel(
    token,
    team_id,
    "Moderado"
)