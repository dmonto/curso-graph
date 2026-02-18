import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def list_plan_buckets(access_token, plan_id):
    """Lista todos los buckets de un plan."""
       
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        buckets = response.json().get("value", [])
        
        result = []
        for bucket in buckets:
            result.append({
                "id": bucket.get("id"),
                "name": bucket.get("name"),
                "planId": bucket.get("planId")
            })
        
        print(f"✓ {len(result)} buckets encontrados")
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