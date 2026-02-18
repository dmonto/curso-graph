import requests
import os
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from A1_8_list_bucket_tasks import list_bucket_tasks
from dotenv import load_dotenv

load_dotenv()

def update_task(access_token, task_id, updates):
    """Actualiza una tarea existente."""
        
    # Primero obtener la tarea actual (necesitamos etag)
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"No se puede obtener tarea: {response.text}")
    
    current_task = response.json()
    etag = response.headers.get("ETag")
    
    # Actualizar
    headers_patch = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}",
        headers=headers_patch,
        json=updates,
        timeout=30
    )
    
    if response.status_code == 204:
        print(f"✓ Tarea actualizada")
        return "OK"
    else:
        print(response.text)
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
buckets = list_plan_buckets(token, plan_id)
for bucket in buckets:
    print(f"  {bucket['name']}: {bucket['id']}")
    
bucket_id = os.getenv("BUCKET_ID") or input("ID de Bucket: ")
tasks = list_bucket_tasks(token, bucket_id)
for task in tasks:
    print(f"  {task['title']}: {task['status']} ({task['percentComplete']}%) - {task['id']}")
task_id = os.getenv("TASK_ID") or input("ID de Task: ")
updates = {
    "percentComplete": 50,
    "status": "inProgress"
}

task = update_task(token, task_id, updates)