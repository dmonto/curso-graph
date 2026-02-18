import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_plan(access_token, plan_id):
    """Obtiene detalles de un plan."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        plan = response.json()
        return {
            "id": plan.get("id"),
            "title": plan.get("title"),
            "owner": plan.get("owner"),
            "created": plan.get("createdDateTime"),
            "modified": plan.get("modifiedDateTime")
        }
    else:
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
plan_info = get_plan(token, plan_id)
print(plan_info)