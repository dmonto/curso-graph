import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

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

# USO
buckets_names = ["Planificación", "Ejecución", "Testing", "Cierre"]

buckets = {}
token = get_apponly_token()

plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
for name in buckets_names:
    bucket = create_bucket(token, plan_id, name)
    buckets[name] = bucket["id"]