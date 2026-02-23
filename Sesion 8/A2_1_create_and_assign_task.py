import requests
import os
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from dotenv import load_dotenv

load_dotenv()

def get_user_id(token, upn):
    r = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{upn}?$select=id",
        headers={"Authorization": f"Bearer {token}"}
    )
    r.raise_for_status()
    return r.json()["id"]

def create_and_assign_task(access_token, plan_id, bucket_id, 
                          task_title, assigned_to_email):
    """Crea tarea y la asigna a un usuario."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Crear tarea
    payload = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": task_title,
        "assignments": {
            get_user_id(access_token, assigned_to_email): {
                "@odata.type": "#microsoft.graph.plannerAssignment",
                "orderHint": " !"
            }
        }
    }
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/planner/tasks",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        task = response.json()
        print(f"✓ Tarea '{task['title']}' asignada a {assigned_to_email}")
        return task
    else:
        print(payload)
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
buckets = list_plan_buckets(token, plan_id)
print(buckets)
bucket_id = os.getenv("BUCKET_ID") or input("Id de Bucket:")

task = create_and_assign_task(
    token, plan_id, bucket_id,
    "Implementar API Graph Test",
    "test@cursograph.onmicrosoft.com"
)