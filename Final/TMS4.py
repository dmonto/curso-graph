import requests
import os
import json
from A0_1_get_delegated_token import get_delegated_token
from A0_1_get_token import get_apponly_token

STATE_FILE = "estado_asignaciones.json"

def load_state():
    """Carga el estado de asignaciones notificadas."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    """Guarda el estado de asignaciones notificadas."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def get_user_info(access_token, user_id):
    """Obtiene información básica de un usuario."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}",
        headers=headers,
        timeout=30
    )
    if response.status_code == 200:
        return response.json()
    return None

def list_plan_buckets(access_token, plan_id):
    """Lista todos los buckets de un plan."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets",
        headers=headers,
        timeout=30
    )
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"Error listando buckets: {response.text}")
        return []

def list_bucket_tasks(access_token, bucket_id):
    """Lista todas las tareas de un bucket."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/buckets/{bucket_id}/tasks",
        headers=headers,
        timeout=30
    )
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"Error listando tareas: {response.text}")
        return []

def send_mention_message(access_token, team_id, channel_id, user_id, user_name, task_title):
    """Publica un mensaje mencionando a un usuario sobre su nueva tarea."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    html_content = f'Hola <at id="0">{user_name}</at>, tienes una nueva tarea asignada: <b>{task_title}</b>'
    
    payload = {
        "body": {
            "contentType": "html",
            "content": html_content
        },
        "mentions": [
            {
                "id": 0,
                "mentionText": user_name,
                "mentioned": {
                    "user": {
                        "id": user_id,
                        "displayName": user_name
                    }
                }
            }
        ]
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    if response.status_code != 201:
        print(f"Error enviando mensaje: {response.text}")
    return response.status_code == 201

if __name__ == "__main__":
    # Scopes necesarios para Delegated (recomendado para este caso)
    SCOPES = ["Tasks.Read", "User.Read.All", "ChannelMessage.Send"]
    
    try:
        token = get_delegated_token(SCOPES)
        
        plan_id = os.getenv("PLAN_ID") or input("Id de Plan: ")
        team_id = os.getenv("TEAM_ID") or input("Id de Team: ")
        channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel: ")

        state = load_state()
        buckets = list_plan_buckets(token, plan_id)
        notificadas_ahora = 0

        print(f"Buscando nuevas asignaciones en {len(buckets)} buckets...")

        for bucket in buckets:
            tasks = list_bucket_tasks(token, bucket["id"])
            for task in tasks:
                task_id = task["id"]
                task_title = task["title"]
                assignments = task.get("assignments", {})
                
                for assigned_user_id in assignments:
                    # Comprobar si esta asignación específica ya fue notificada
                    state_key = f"{task_id}_{assigned_user_id}"
                    
                    if state_key not in state:
                        print(f"Nueva asignación detectada: '{task_title}' para {assigned_user_id}")
                        
                        user_info = get_user_info(token, assigned_user_id)
                        if user_info:
                            user_name = user_info.get("displayName", "Compañero")
                            success = send_mention_message(token, team_id, channel_id, assigned_user_id, user_name, task_title)
                            
                            if success:
                                print(f"Notificación enviada a {user_name}")
                                state[state_key] = True
                                notificadas_ahora += 1
                            else:
                                print(f"Falló el envío a Teams")
                        else:
                            print(f"No se pudo obtener el nombre del usuario")

        if notificadas_ahora > 0:
            save_state(state)
            print(f"\n--- Éxito: {notificadas_ahora} nuevas notificaciones enviadas. ---")
        else:
            print("\n--- No hay nuevas asignaciones. ---")
            
    except Exception as e:
        print(f"ERROR: {e}")