import requests
import os
from A0_1_get_token import get_apponly_token

def get_team_members(access_token, team_id):
    """Obtiene todos los miembros del equipo."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/members",
        headers=headers,
        params={"$select": "id,displayName,roles"},
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        members = response.json().get("value", [])
        return [
            {
                "id": member["id"],
                "name": member.get("displayName"),
                "email": member.get("email"),
                "roles": member.get("roles", [])
            }
            for member in members
        ]
    
    return []

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
members = get_team_members(token, team_id)
for member in members:
    role = "Propietario" if "owner" in member["roles"] else "Miembro"
    print(f"- {member['name']}/{member['id']} ({role})")