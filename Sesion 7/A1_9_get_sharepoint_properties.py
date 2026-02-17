import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def muestra_listas(access_token, site_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists",
        headers=headers,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        items = response.json()['value']
        print("Listas")
        print([f"{it['id']}/{it['displayName']}" for it in items])

def muestra_items(access_token, site_id, list_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items",
        headers=headers,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        items = response.json()['value']
        print("Listas")
        print([f"{it['id']}/{it['webUrl']}" for it in items])

def get_sharepoint_properties(access_token, site_id, list_id, item_id):
    """Obtiene propiedades personalizadas de un elemento en SharePoint."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}",
        headers=headers,
        timeout=30
    )
    print(response.json())

    if response.status_code == 200:
        item = response.json()
        return {
            "id": item["id"],
            "fields": item.get("fields", {}),  # Propiedades personalizadas
            "created": item.get("createdDateTime"),
            "modified": item.get("lastModifiedDateTime")
        }
    
    return None

# USO
token = get_apponly_token()
site_id = os.getenv("SITE_ID") or input("Id de Site:")
muestra_listas(token, site_id)

list_id = os.getenv("LIST_ID") or input("Id de Lista:")
muestra_items(token, site_id, list_id)

item_id = os.getenv("SHARE_ITEM_ID") or input("Id de Sharepoint Item:")
props = get_sharepoint_properties(token, site_id, list_id, item_id)
print(f"Propiedades: {props['fields']}")