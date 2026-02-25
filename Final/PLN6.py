import requests
import os
from A0_1_get_token import get_apponly_token
from A0_1_get_delegated_token import get_delegated_token
from dotenv import load_dotenv

load_dotenv()

def create_plan(access_token, group_id, plan_title, plan_description=""):
    """Crea un nuevo plan en un grupo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": plan_title,
        "owner": group_id  # ID del grupo Microsoft 365
    }
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/planner/plans",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        plan = response.json()
        print(f"✓ Plan creado: {plan['title']}")
        print(f"  ID: {plan['id']}")
        return plan
    else:
        raise Exception(f"Error: {response.text}")


def create_bucket(access_token, plan_id, bucket_name):
    """Crea un nuevo bucket en un plan."""
        
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": bucket_name,
        "planId": plan_id
    }
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/planner/buckets",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        bucket = response.json()
        print(f"✓ Bucket creado: {bucket['name']}")
        print(f"  ID: {bucket['id']}")
        return bucket
    else:
        raise Exception(f"Error: {response.text}")


def send_message(access_token, team_id, channel_id, message_text):
    """Publica un mensaje simple en un canal."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "body": {
            "contentType": "text",
            "content": message_text
        }
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.json())
    if response.status_code == 201:
        message = response.json()
        return {
            "status": "success",
            "message_id": message["id"],
            "timestamp": message.get("createdDateTime")
        }
    else:
        return {
            "status": "failed",
            "error": response.json()
        }

# USO
token = get_apponly_token()
group_id = os.getenv("GROUP_ID") or input("Id de Grupo:")
nombre_plan = input("Nombre del Plan:")
plan = create_plan(token, group_id, nombre_plan, "Configuración de plan")
plan_id = plan["id"]


buckets_names = ["Desarrollo", "Pruebas", "Produccion"]

buckets = {}

########plan_id = input("Id de Plan:")

for name in buckets_names:
    bucket = create_bucket(token, plan_id, name)
    buckets[name] = bucket["id"]


# TEAM ID 12801113-b209-4db2-bf9a-835822f0f237
# CHANNEL ID 19:25bc601a6f9848ca8ad2cc185b220ad3@thread.tacv2

SCOPES = ["ChannelMessage.Send"]
token = get_delegated_token(SCOPES)
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
result = send_message(
    token,
    team_id,
    channel_id,
    "He realizado la tarea PLN6 - Configuración de Plan"
)

print(f"Mensaje enviado: {result['message_id']}")