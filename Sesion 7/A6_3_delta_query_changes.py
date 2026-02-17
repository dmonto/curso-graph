import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def delta_query_changes(access_token, delta_link):
    """Obtiene solo cambios desde último delta."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    changes = {
        "added": [],
        "modified": [],
        "deleted": []
    }
    new_delta_link = None
    
    url = delta_link
    
    while url:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        for item in data.get("value", []):
            if "@removed" in item:
                # Elemento eliminado
                changes["deleted"].append(item["id"])
            elif item.get("createdDateTime"):
                # Elemento nuevo o modificado
                if len(changes["added"]) == 0:
                    changes["added"].append(item)
                else:
                    changes["modified"].append(item)
        
        if "@odata.deltaLink" in data:
            new_delta_link = data["@odata.deltaLink"]
        
        url = data.get("@odata.nextLink")
    
    return {
        "changes": changes,
        "new_delta_link": new_delta_link
    }

# USO
token = get_apponly_token()
delta_link = os.getenv("DELTA_LINK") or input("Delta Link:")
result = delta_query_changes(token, delta_link)
print(f"Nuevos: {len(result['changes']['added'])}")
print(f"Modificados: {len(result['changes']['modified'])}")
print(f"Eliminados: {len(result['changes']['deleted'])}")
print(f"Nuevo Link: {result['new_delta_link']}")