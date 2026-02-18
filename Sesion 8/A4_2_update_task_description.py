import requests
import os
from dotenv import load_dotenv
from A0_1_get_token import get_apponly_token

load_dotenv()

def update_task_description(token, task_id, etag, new_description):
    """Actualiza descripción de tarea."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {token}"}
        
    # Actualizar
    headers_patch = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }
    
    r = requests.patch(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
        headers=headers_patch,
        json={"description": new_description},
        timeout=30
    )
    
    if r.status_code in [200, 204]:
        print(f"✓ Descripción actualizada")
    else:
        raise Exception(f"Error: {r.text}")

# USO
token = get_apponly_token()
task_id = os.getenv("TASK_ID") or input("Id de Task:")
etag = input("eTag:")
update_task_description(token, task_id, etag, "Nueva descripción")