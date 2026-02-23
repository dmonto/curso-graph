import requests
import uuid
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def regenerate_orderhint(checklist):
    sorted_items = sorted(checklist.items(), key=lambda x: x[1]["orderHint"])
    reversed_items = list(reversed(sorted_items))
    new_check = {}
    prev_hint = "" 
    
    for k, v in reversed_items:
        if prev_hint:
            hint_formula = f"X{prev_hint} !"  
            prev_hint = hint_formula[1:]
        else:
            hint_formula = " !"  # Primer ítem
            prev_hint = hint_formula
        
        new_check[k] = {
            "@odata.type": "#microsoft.graph.plannerChecklistItem",
            "title": v["title"],
            "isChecked": v["isChecked"],
            "orderHint": hint_formula  
        }
    return new_check

def show_checklist(token, task_id):
    """Lista con IDs y orderHints."""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details?$select=checklist", headers=headers)
    if resp.status_code == 200:
        cl = resp.json().get("checklist", {})
        print("\n📋 Checklist:")
        for iid, item in sorted(cl.items(), key=lambda x: x[1].get('orderHint', '')):
            status = "✅" if item["isChecked"] else "❌"
            print(f"  {iid} | {status} {item['title'][:30]}... | {item['orderHint']}")
        return cl
    else:
        print("❌", resp.text)

def reset_checklist_clean(token, task_id, items):
    """RESET total + items nuevos."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    resp = requests.get(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details", headers=headers)
    etag = resp.headers.get("ETag", "")
    details = resp.json()
    checklist = details.get("checklist", {})
    patch_headers = headers.copy()
    patch_headers["If-Match"] = etag
    for i, it in enumerate(items):
        iid = str(uuid.uuid4())
        checklist[iid] = {"@odata.type": "#microsoft.graph.plannerChecklistItem", "title": it, "isChecked": False, "orderHint": f"ZZZ{i}"}
    checklist = regenerate_orderhint(checklist)
    print(checklist)

    resp = requests.patch(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
                          headers=patch_headers, json={"checklist": checklist})
    print(resp.text)
    print(f"✅ Checklist RESET: {len(checklist)} items")    
    print("\n📋 Checklist actual con IDs:")
    show_checklist(token, task_id)

# USO
if __name__ == "__main__":
    token = get_apponly_token()
    task_id = input("Task ID: ")
    items = ["6. Documentación"]
    reset_checklist_clean(token, task_id, items)
