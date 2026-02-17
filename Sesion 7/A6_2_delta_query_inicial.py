import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def delta_query_initial(access_token, drive_id):
    """Primera delta query para obtener estado inicial."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    all_items = []
    delta_link = None
    
    # Primera llamada con /delta
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root/delta"
    
    while url:
        response = requests.get(url, headers=headers, timeout=30)
        print(response.json())
        response.raise_for_status()
        
        data = response.json()
        items = data.get("value", [])
        
        all_items.extend(items)
        print(f"✓ Obtenidos {len(all_items)} elementos")
        
        # Token para próxima sincronización
        if "@odata.deltaLink" in data:
            delta_link = data["@odata.deltaLink"]
        
        # Siguiente página
        url = data.get("@odata.nextLink")
    
    return {
        "items": all_items,
        "delta_link": delta_link
    }

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
result = delta_query_initial(token, drive_id)
print(f"Estado inicial: {len(result['items'])} elementos")
print(f"Delta link: {result['delta_link']}")