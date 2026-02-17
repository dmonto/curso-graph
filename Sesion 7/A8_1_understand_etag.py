import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def understand_etag(access_token, drive_id, item_id):
    """Explica ETags."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 1. OBTENER item con ETag
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers,
        timeout=30
    )
    print(response.json())

    item = response.json()    
    print(f"ETag actual: {item.get('eTag')}")
    print(f"Última modificación: {item.get('lastModifiedDateTime')}")
    
    # 2. MODIFICAR con If-Match (optimistic locking)
    updates = {"name": "sesion-5.md"}
    
    # IMPORTANTE: incluir ETag en If-Match
    headers_update = {
        **headers,
        "If-Match": item.get("eTag"),  # ETag actual
        "Content-Type": "application/json"
    }
    
    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
        headers=headers_update,
        json=updates,
        timeout=30
    )
    print(response.json())
    if response.status_code == 200:
        print("✓ Actualización exitosa")
    elif response.status_code == 412:
        print("✗ Conflicto de ETag (item cambió)")
        # Obtener última versión
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
            headers=headers,
            timeout=30
        )
        latest = response.json()
        print(f"Última versión obtenida")
        return latest
    
    return response.json()

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
result = understand_etag(token, drive_id, item_id)