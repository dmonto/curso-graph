import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def get_item_thumbnails(access_token, drive_id, item_id, sizes=["small", "medium", "large"]):
    """Obtiene vistas previas (thumbnails) del elemento."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/thumbnails",
        headers=headers,
        timeout=30
    )
    print(response.json())
    
    if response.status_code == 200:
        thumbnails_data = response.json().get("value", [])
        
        result = {}
        for thumbnail_set in thumbnails_data:
            for size in sizes:
                if size in thumbnail_set:
                    result[size] = {
                        "url": thumbnail_set[size].get("url"),
                        "width": thumbnail_set[size].get("width"),
                        "height": thumbnail_set[size].get("height")
                    }
        
        return result
    
    return {}

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
thumbnails = get_item_thumbnails(token, drive_id, item_id)
for size, data in thumbnails.items():
    print(f"{size}: {data['width']}x{data['height']} - {data['url']}")