import requests
import os
from A0_1_get_token import get_apponly_token

def update_member_role(access_token, team_id, member_id, roles):
    """Actualiza el rol de un miembro."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember", 
        "roles": roles  # ["owner"] o ["member"]
    } 
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/members/{member_id}",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    return response.status_code == 200

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
member_id = os.getenv("MEMBER_ID") or input("Id de Member:")

# Promover a propietario
update_member_role(token, team_id, member_id, ["owner"])

# Degradar a miembro
update_member_role(token, team_id, member_id, ["member"])