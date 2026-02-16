import requests
import os
from A0_1_get_token import get_apponly_token

def create_private_channel(access_token, team_id, channel_name, owner_ids):
    """Crea un canal privado con propietarios específicos."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "displayName": channel_name,
        "membershipType": "private",
        "owners@odata.bind": [
            f"https://graph.microsoft.com/v1.0/users('{user_id}')"
            for user_id in owner_ids
        ]
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
create_private_channel(
    token,
    team_id,
    "estrategia",
    owner_ids=["user_id_1", "user_id_2"]
)