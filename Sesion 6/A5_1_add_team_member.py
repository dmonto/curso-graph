import requests
import os
from A0_1_get_token import get_apponly_token

def add_team_member(access_token, team_id, user_id):
    """Añade un usuario al equipo como miembro."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id}')",
        "roles": ["member"]
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/members",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print(response.json())
    return response.status_code == 201

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
user_id = os.getenv("USER_ID") or input("Id de User:")
print(add_team_member(token, team_id, user_id))