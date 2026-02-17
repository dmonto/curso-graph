import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def paginate_drive(token, drive_id, folder_id="root", max_items=None):
    """Paginación correcta DriveItems."""
    headers = {"Authorization": f"Bearer {token}"}
    all_items = []
    
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children?$top=1000"
    
    while url:
        response = requests.get(url, headers=headers, timeout=30)
        print(response.json())
        response.raise_for_status()
        
        data = response.json()
        items = data.get("value", [])
        all_items.extend(items)
        print(f"📁 {len(items)} items → Total: {len(all_items)}")
        
        if max_items and len(all_items) >= max_items:
            return all_items[:max_items]
        
        url = data.get("@odata.nextLink")
       
    return all_items

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
items = paginate_drive(token, drive_id, max_items=10000)
print(f"Total: {len(items)}")