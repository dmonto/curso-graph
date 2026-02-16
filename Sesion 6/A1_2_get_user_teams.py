import requests
import re
from A0_1_get_token import get_delegated_token

def get_user_teams(access_token):
    """Obtiene todos los equipos a los que pertenece el usuario."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/joinedTeams",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        teams = response.json().get("value", [])
        return [
            {
                "id": team["id"],
                "name": team["displayName"],
                "description": team.get("description", "")
            }
            for team in teams
        ]
    
    return []

# USO
SCOPES = ["Team.ReadBasic.All"]
token = get_delegated_token(SCOPES)
teams = get_user_teams(token)
for team in teams:
    print(f"- {team['name']} ({team['id']})")