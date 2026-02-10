import os
import json
import logging
from datetime import datetime
from msal import ConfidentialClientApplication
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_app_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def export_group_hierarchy(filename: str = None):
    """Exportar grupos y sus miembros (estructura jerárquica JSON)."""
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    if not filename:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"groups_hierarchy_{timestamp}.json"
    
    export_start = datetime.utcnow()
    groups_data = []
    
    try:
        # Paso 1: obtener todos los grupos
        url = "https://graph.microsoft.com/v1.0/groups?$select=id,displayName,mail,groupTypes&$top=50"
        all_groups = []
        
        while url:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            all_groups.extend(data.get('value', []))
            url = data.get('@odata.nextLink')
        
        logger.info(f"Descargados {len(all_groups)} grupos")
        
        # Paso 2: para cada grupo, obtener miembros
        for group in all_groups:
            group_id = group['id']
            members_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=id,displayName,userPrincipalName"
            
            members = []
            while members_url:
                resp = requests.get(members_url, headers=headers, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                members.extend(data.get('value', []))
                members_url = data.get('@odata.nextLink')
            
            group_with_members = {
                **group,
                "members": members,
                "member_count": len(members),
            }
            groups_data.append(group_with_members)
            logger.info(f"  {group['displayName']}: {len(members)} miembros")
        
        # Paso 3: estructura con metadata
        export_doc = {
            "export_metadata": {
                "timestamp": export_start.isoformat() + "Z",
                "source": "Microsoft Graph",
                "resource": "groups_with_members",
                "group_count": len(groups_data),
                "format_version": "1.0",
            },
            "data": groups_data,
        }
        
        # Escribir JSON
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_doc, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Exportación jerárquica completada")
        logger.info(f"  Archivo: {filename}")
        logger.info(f"  Grupos: {len(groups_data)}")
        
        return {"filename": filename, "group_count": len(groups_data)}
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    result = export_group_hierarchy()
    print(f"Resultado: {result}")