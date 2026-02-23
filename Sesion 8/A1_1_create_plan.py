import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def create_plan(access_token, group_id, plan_title, plan_description=""):
    """Crea un nuevo plan en un grupo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": plan_title,
        "owner": group_id  # ID del grupo Microsoft 365
    }
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/planner/plans",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        plan = response.json()
        print(f"✓ Plan creado: {plan['title']}")
        print(f"  ID: {plan['id']}")
        return plan
    else:
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
group_id = os.getenv("GROUP_ID") or input("Id de Grupo:")
plan = create_plan(token, group_id, "Proyecto Diego 2026", "Planificación trimestral")
plan_id = plan["id"]