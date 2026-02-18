import requests
import os
from dotenv import load_dotenv
from A0_1_get_token import get_apponly_token

load_dotenv()

def get_all_tasks(token, plan_id):
    """Obtiene todas las tareas del plan."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {token}"}
    
    r = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/tasks",
        headers=headers,
        timeout=30
    )
    
    if r.status_code == 200:
        tasks = r.json().get("value", [])
        print(f"✓ {len(tasks)} tareas obtenidas")
        return tasks
    else:
        raise Exception(f"Error: {r.text}")

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
    tasks = get_all_tasks(token, plan_id)