import requests
from A0_1_get_token import get_delegated_token  

SCOPES = ["Files.ReadWrite.All"]  # Para OneDrive completo

def one_drive_requests(token):
    """Operaciones OneDrive con requests puro."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🔍 **Mi OneDrive**")
    
    # 1. Mi Drive info
    r = requests.get("https://graph.microsoft.com/v1.0/me/drive", headers=headers)
    drive = r.json()
    print(f"Drive ID: {drive['id']}")
    print(f"Quota: {drive['quota']['total']} total / {drive['quota']['remaining']} libre")
    print()
    
    # 2. Listar archivos raíz
    print("📁 **Archivos raíz**")
    r = requests.get("https://graph.microsoft.com/v1.0/me/drive/root/children", headers=headers)
    items = r.json()["value"]
    for item in items[:10]:  # Top 10
        size = item.get('size', 0)
        print(f"  {item['name']} ({size:,} bytes) - {item.get('file', {}).get('mimeType', 'Carpeta')}")
    print()
    
    # 3. Archivo específico (usa el primero como ejemplo)
    if items:
        item_id = items[0]['id']
        print(f"📄 **Detalles: {items[0]['name']}**")
        r = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}", headers=headers)
        file_item = r.json()
        print(f"  ID: {file_item['id']}")
        print(f"  Modificado: {file_item['lastModifiedDateTime']}")
        print(f"  Autor: {file_item.get('lastModifiedBy', {}).get('user', {}).get('displayName', 'N/A')}")
        print()
        
        # 4. Crear link compartible
        print("🔗 **Creando link compartible**")
        share_payload = {
            "type": "view",
            "scope": "organization"  # organization, anonymous, users
        }
        r = requests.post(
            f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/createLink",
            headers=headers,
            json=share_payload
        )
        share_link = r.json()
        print(f"  ✅ Link: {share_link['link']['webUrl']}")
        print(f"  Tipo: {share_link['link']['type']} / Scope: {share_link['link']['scope']}")
    else:
        print("No hay archivos para mostrar")

# USO
token = get_delegated_token(SCOPES)
one_drive_requests(token)
