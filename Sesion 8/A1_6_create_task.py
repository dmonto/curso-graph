import requests
import os
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from dotenv import load_dotenv

load_dotenv()

def create_task(access_token, plan_id, bucket_id, task_title, 
                assigned_to=None, due_date=None, priority=3):
    """Crea una nueva tarea en un bucket."""
        
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": task_title,
        "priority": priority  # 0-5 (más bajo = más prioritario)
    }
    
    # Opcional: fecha de vencimiento
    if due_date:
        payload["dueDateTime"] = due_date
    
    # Opcional: asignado a
    if assigned_to:
        payload["assignedTo"] = assigned_to
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/planner/tasks",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        task = response.json()
        print(f"✓ Tarea creada: {task['title']}")
        print(f"  ID: {task['id']}")
        return task
    else:
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
buckets = list_plan_buckets(token, plan_id)
bucket_id = os.getenv("BUCKET_ID") or input("Id de Bucket:")
task = create_task(
    token, plan_id, bucket_id,
    "Especificaciones técnicas",
    due_date="2026-02-28",
    priority=1
)
task_id = task["id"]