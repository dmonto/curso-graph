import requests
import os
from dotenv import load_dotenv
from A0_1_get_token import get_apponly_token

load_dotenv()

def get_task(token, task_id):
    """Obtiene tarea y captura ETag."""
    
    headers = {"Authorization": f"Bearer {token}"}
    
    r = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
        headers=headers,
        timeout=30
    )
    
    if r.status_code == 200:
        task = r.json()
        etag = r.headers.get("ETag")
        
        print(f"✓ Tarea: {task['description']}")
        print(f"  ETag: {etag}")
        
        return task, etag
    else:
        raise Exception(f"Error: {r.text}")

# USO
token = get_apponly_token()
task_id = os.getenv("TASK_ID") or input("Id de Task:")
task, etag = get_task(token, task_id)