import requests
import uuid
from A0_1_get_token import get_apponly_token
from A1_10_add_checklist_item import regenerate_orderhint, show_checklist
from dotenv import load_dotenv

load_dotenv()

def mark_checklist_item(token, task_id, item_id, is_checked=True):
    """Marca ✓️ SIN tocar orderHint (evita error)."""
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details?$select=checklist", headers=headers)
    if resp.status_code != 200:
        print(f"❌ GET: {resp.text}")
        return
    
    details = resp.json()
    etag = resp.headers.get("ETag")
    checklist = details.get("checklist", {})
    
    if item_id not in checklist:
        print(f"❌ ID '{item_id}' no existe")
        return
    
    item = checklist[item_id]
    item["isChecked"] = is_checked  
    checklist=regenerate_orderhint(checklist)

    patch_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "If-Match": etag}
    resp = requests.patch(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
                          headers=patch_headers, json={"checklist": checklist})
    
    status = "✓️ completado" if is_checked else "⭕ pendiente"
    if resp.status_code == 200:
        print(f"✅ '{item['title']}' → {status} (orderHint '{item['orderHint']}' preservado)")
    else:
        print(f"❌ PATCH: {resp.text}")

# USO COMPLETO
token = get_apponly_token()
task_id = input("Task ID: ")

print("1️⃣ Lista actual:")
show_checklist(token, task_id)

print("\n3️⃣ Marca item (ID): ")
item_id = input()
mark_checklist_item(token, task_id, item_id, True)
show_checklist(token, task_id)
