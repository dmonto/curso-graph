import requests
import os
from A0_1_get_token import get_apponly_token

def update_team(access_token, team_id, **updates):
    """Actualiza propiedades del equipo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}",
        headers=headers,
        json=updates,
        timeout=30
    )
    
    return response.status_code == 200

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
update_team(
    token,
    team_id,
    displayName="Team del 16_Feb",
    description="Descripción"
)