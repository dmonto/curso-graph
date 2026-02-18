import requests
import os
import json
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from dotenv import load_dotenv

load_dotenv()

def create_task_complete(access_token, plan_id, bucket_id, user_id, task_data):
    """Crea tarea Planner con validación de open types y todos los parámetros."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Payload base (solo propiedades simples)
    payload = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": task_data.get("title", "Tarea sin título"),
        "priority": task_data.get("priority"),  # 0-11, entero
        "description": task_data.get("description", ""),
        "percentComplete": task_data.get("percentComplete", 0)
    }
    
    # DueDate como ISO string
    if task_data.get("dueDate"):
        try:
            # Asegura formato ISO 8601
            due_date = task_data["dueDate"]
            if isinstance(due_date, str):
                payload["dueDateTime"] = due_date  # Espera "2026-02-15T17:00:00Z"
            else:
                payload["dueDateTime"] = due_date.isoformat() + "Z"
        except:
            print("⚠️ dueDate inválido, omitido")
    
    if user_id:
        payload["assignments"] = {
            user_id: {  
                "@odata.type": "#microsoft.graph.plannerAssignment",
                "orderHint": " !"  
            }
        }
    
    # LOGGING para debug
    print("📋 Payload enviado:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/planner/tasks",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        task = response.json()
        print("✅ Tarea creada:", task["title"], f"(ID: {task['id'][:8]}...)")
        return task
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text)
        raise Exception(f"Error Graph: {response.text}")

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    
    # Listar planes/buckets si no proporcionados
    plan_id = os.getenv("PLAN_ID") or input("ID de Plan: ")
    print("📂 Listando planes y buckets...")

    list_plan_buckets(token, plan_id)
    
    bucket_id = os.getenv("BUCKET_ID") or input("ID de Bucket: ")
    user_id = os.getenv("USER_ID") or input("ID de Usuario: ")
    
    task_data = {
        "title": "Implementar API REST",
        "description": "Crear endpoints para CRUD de sitios SharePoint",
        "priority": 1,  # Urgente
        "dueDate": "2026-02-20T17:00:00Z",  # ISO con Z
        "assignedTo": "test@cursograph.onmicrosoft.com",  # Email válido
        "percentComplete": 0
    }
    
    try:
        task = create_task_complete(token, plan_id, bucket_id, user_id, task_data)
        print(f"🎉 ¡Tarea creada exitosamente! {task['id']}")
    except Exception as e:
        print("💥 Falló:", str(e))