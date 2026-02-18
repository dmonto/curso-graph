import requests
import os
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from dotenv import load_dotenv

load_dotenv()

def create_plan_labels(access_token, plan_id, labels):
    """Crea etiquetas en un plan."""
    
    import requests
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Obtener plan
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Error obteniendo plan: {response.text}")
    
    plan = response.json()
    etag = response.headers.get("ETag")
    
    # Crear estructura de etiquetas
    label_definitions = {}
    
    for i, label in enumerate(labels):
        label_id = str(i)
        label_definitions[label_id] = {
            "displayName": label,
            "color": i % 6  # Colores 0-5
        }
    
    # Actualizar plan con etiquetas
    headers_patch = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}",
        headers=headers_patch,
        json={"categoryDescriptions": label_definitions},
        timeout=30
    )
    
    if response.status_code in [200, 204]:
        print(f"✓ {len(labels)} etiquetas creadas")
        return
    else:
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")

labels = [
    "Urgente",
    "Backend",
    "Frontend",
    "Testing",
    "Documentación",
    "Deploy"
]

plan = create_plan_labels(token, plan_id, labels)