import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def get_all_permissions(access_token, drive_id, item_id):
    """Obtiene todos los permisos de un elemento."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/permissions",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        permissions = response.json().get("value", [])
        
        result = []
        for perm in permissions:
            perm_info = {
                "id": perm["id"],
                "roles": perm.get("roles", []),
                "grantedTo": None,
                "type": "link"
            }
            
            # Usuario directo
            if "grantedToV2" in perm and "user" in perm["grantedToV2"]:
                user = perm["grantedToV2"]["user"]
                perm_info["grantedTo"] = user.get("displayName")
                perm_info["email"] = user.get("mail")
                perm_info["type"] = "user"
            
            # Grupo
            elif "grantedToV2" in perm and "group" in perm["grantedToV2"]:
                group = perm["grantedToV2"]["group"]
                perm_info["grantedTo"] = group.get("displayName")
                perm_info["type"] = "group"
            
            # Enlace
            elif "link" in perm:
                perm_info["type"] = "link"
                perm_info["scope"] = perm["link"].get("scope")
                perm_info["expirationDateTime"] = perm.get("link").get("expirationDateTime")
            
            result.append(perm_info)
        
        return result
    
    return []

# USO
token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
item_id = os.getenv("ITEM_ID") or input("Id de Item:")
permissions = get_all_permissions(token, drive_id, item_id)
print(f"Total de permisos: {len(permissions)}\n")
for perm in permissions:
    print(f"{perm['type'].upper()}: {perm.get('grantedTo', 'Enlace')}")
    print(f"  Rol: {perm['roles']}")
    print(f"  ID: {perm['id']}\n")
    print(f"  Scope: {perm.get('scope')}\n")
    print(f"  Expiration: {perm.get('expirationDateTime')}\n")