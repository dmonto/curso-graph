import requests
import os
import json
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from dotenv import load_dotenv

load_dotenv()

def list_bucket_tasks(access_token, bucket_id):
    """Lista todas las tareas de un bucket."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/buckets/{bucket_id}/tasks",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        tasks = response.json().get("value", [])
        
        result = []
        for task in tasks:
            result.append({
                "id": task.get("id"),
                "title": task.get("title"),
                "status": task.get("status"),
                "priority": task.get("priority"),
                "percentComplete": task.get("percentComplete"),
                "dueDate": task.get("dueDateTime")
            })
        
        print(f"✓ {len(result)} tareas encontradas")
        return result
    else:
        raise Exception(f"Error: {response.text}")

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
    buckets = list_plan_buckets(token, plan_id)
    for bucket in buckets:
        print(f"  {bucket['name']}: {bucket['id']}")
        
    bucket_id = os.getenv("BUCKET_ID") or input("ID de Bucket: ")
    tasks = list_bucket_tasks(token, bucket_id)
    for task in tasks:
        print(f"  {task['title']}: {task['status']} ({task['percentComplete']}%) - {task['id']}")