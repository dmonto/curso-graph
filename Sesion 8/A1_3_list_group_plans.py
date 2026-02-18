import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def list_group_plans(access_token, group_id):
    """Lista todos los planes de un grupo."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Primero obtener planes del grupo
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/groups/{group_id}/planner/plans",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        plans = response.json().get("value", [])
        
        result = []
        for plan in plans:
            result.append({
                "id": plan.get("id"),
                "title": plan.get("title"),
                "created": plan.get("createdDateTime")
            })
        
        print(f"✓ {len(result)} planes encontrados")
        return result
    else:
        raise Exception(f"Error: {response.text}")

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    group_id = os.getenv("GROUP_ID") or input("Id de Grupo:")
    plans = list_group_plans(token, group_id)
    print(plans)