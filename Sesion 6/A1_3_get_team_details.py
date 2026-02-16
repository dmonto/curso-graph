import requests
import os
from A0_1_get_token import get_apponly_token

def get_team_details(access_token, team_id):
    """Obtiene información detallada de un equipo."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}",
        headers=headers,
        params={"$select": "id,displayName,description,visibility,createdDateTime,memberSettings"},
        timeout=30
    )
    
    if response.status_code == 200:
        team = response.json()
        return {
            "id": team["id"],
            "name": team["displayName"],
            "description": team.get("description"),
            "visibility": team.get("visibility"),
            "created": team.get("createdDateTime"),
            "settings": team.get("memberSettings", {})
        }
    
    return None

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
details = get_team_details(token, team_id)
print(f"Nombre: {details['name']}")
print(f"Visibilidad: {details['visibility']}")