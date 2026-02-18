import requests
import os
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from dotenv import load_dotenv

load_dotenv()

def assign_labels_to_task(access_token, task_id, label_ids):
    """Asigna etiquetas a una tarea."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener detalles de tarea
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}")
    
    task_details = response.json()
    etag = response.headers.get("ETag")
    
    # Crear estructura de etiquetas
    labels = {}
    for label_id in label_ids:
        labels[label_id] = True
    
    # Actualizar
    headers_patch = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
        headers=headers_patch,
        json={"appliedCategories": labels},
        timeout=30
    )
    
    if response.status_code in [200, 204]:
        print(f"✓ {len(label_ids)} etiquetas asignadas")
        return 
    else:
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
task_id = os.getenv("TASK_ID") or input("Id de Task:")
label_ids = ["0", "1"]  # "Urgente", "Backend"

task_details = assign_labels_to_task(token, task_id, label_ids)