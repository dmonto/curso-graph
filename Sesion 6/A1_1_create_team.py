import requests
import re
from A0_1_get_token import get_apponly_token
import json

def create_team(access_token, team_name, team_description, owner_upn, visibility="private"):
    """Crea un nuevo equipo en Teams con app-only token."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "template@odata.bind": "https://graph.microsoft.com/v1.0/teamsTemplates('standard')",
        "displayName": team_name,
        "description": team_description,
        "visibility": visibility,
        "members": [
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{owner_upn}')"
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://graph.microsoft.com/v1.0/teams",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")  # Debug
        print(f"Headers: {dict(response.headers)}")  # Debug: mira Location/Content-Location
        print(f"Response text: '{response.text}'")  # Debug: verifica body vacío
        
        if response.status_code in [200, 201, 202]:
            # Extrae team_id de Content-Location: /teams('team-id')
            content_location = response.headers.get('Content-Location', '')
            team_id_match = re.search(r"/teams/'([^']+)'", content_location)
            team_id = team_id_match.group(1) if team_id_match else None
            
            return {
                "status": "success",
                "team_id": team_id,
                "location": response.headers.get("Location"),
                "content_location": content_location
            }
        else:
            # Maneja body vacío o no-JSON
            try:
                error_data = response.json()
            except json.JSONDecodeError:
                error_data = {"message": response.text}
            print(f"Error {response.status_code}: {error_data}")
            return {"status": "failed", "error": error_data}
    
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

# USO (ejecuta y comparte los prints de debug)
token = get_apponly_token()
result = create_team(
    token,
    team_name="Proyecto Especial",
    team_description="Equipo para proyecto estratégico",
    owner_upn="diego.montoliu@cursograph.onmicrosoft.com",
    visibility="private"
)
print(f"Resultado: {result}")
