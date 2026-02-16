import requests
import os
from A0_1_get_token import get_apponly_token

def delete_team(access_token, team_id):
    """Elimina un equipo (requiere ser propietario)."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}",
        headers=headers,
        timeout=30
    )
    
    print(response.json())
    return response.status_code == 204

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
success = delete_team(token, team_id)