import requests
import os
from A0_1_get_token import get_apponly_token

def remove_team_member(access_token, team_id, member_id):
    """Elimina un miembro del equipo."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/members/{member_id}",
        headers=headers,
        timeout=30
    )
    
    print(response.json())
    return response.status_code == 204

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
user_id = os.getenv("USER_ID") or input("Id de User:")
remove_team_member(token, team_id, user_id)