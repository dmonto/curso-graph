import requests
import os
from A0_1_get_token import get_delegated_token

def delete_team(access_token, team_id):
    """Elimina un equipo (requiere ser propietario)."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/archive",
        headers=headers
    )
    print(f"Archive: {r.status_code}")

    return r.status_code == 204

# USO
SCOPES=["TeamSettings.ReadWrite.All"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
success = delete_team(token, team_id)