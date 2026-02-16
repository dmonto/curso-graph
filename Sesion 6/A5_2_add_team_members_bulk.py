import requests
import os
from A0_1_get_token import get_apponly_token
from A5_1_add_team_member import add_team_member

def add_team_members_bulk(access_token, team_id, user_ids, as_owner=False):
    """Añade múltiples miembros al equipo en paralelo."""
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    roles = ["owner"] if as_owner else ["member"]
    
    def add_member_task(user_id):
        try:
            success = add_team_member(access_token, team_id, user_id)
        except Exception as e:
            return {"user_id": user_id, "success": False, "error": str(e)}
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(add_member_task, uid) for uid in user_ids]
        for future in as_completed(futures):
            results.append(future.result())
    
    return results

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
user_ids = ["user1", "user2", "user3"]
results = add_team_members_bulk(token, team_id, user_ids, as_owner=False)

for result in results:
    status = "✓" if result["success"] else "✗"
    print(f"{status} {result['user_id']}")