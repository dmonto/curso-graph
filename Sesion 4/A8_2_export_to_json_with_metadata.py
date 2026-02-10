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
EXPORT_USER = os.getenv("EXPORT_USER", "admin@contoso.com")

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

def export_to_json_with_metadata(resource: str = "users", filename: str = None):
    """Exportar usuarios/grupos a JSON con metadata de auditoría."""
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    if not filename:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{resource}_export_{timestamp}.json"
    
    export_start = datetime.utcnow()
    
    # Recopilar datos
    data_list = []
    url = f"https://graph.microsoft.com/v1.0/{resource}?$top=50&$select=id,displayName,mail"
    
    try:
        while url:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            response_data = resp.json()
            
            data_list.extend(response_data.get('value', []))
            url = response_data.get('@odata.nextLink')
            logger.info(f"Descargados {len(data_list)} registros...")
        
        # Construir documento con metadata
        export_doc = {
            "export_metadata": {
                "timestamp": export_start.isoformat() + "Z",
                "exported_by": EXPORT_USER,
                "tenant_id": TENANT_ID,
                "source": "Microsoft Graph",
                "endpoint": f"/{resource}",
                "record_count": len(data_list),
                "format_version": "1.0",
            },
            "data": data_list,
        }
        
        # Escribir a JSON
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_doc, jsonfile, indent=2, ensure_ascii=False)
        
        export_end = datetime.utcnow()
        duration = (export_end - export_start).total_seconds()
        
        logger.info(f"✅ Exportación JSON completada")
        logger.info(f"  Archivo: {filename}")
        logger.info(f"  Registros: {len(data_list)}")
        logger.info(f"  Duración: {duration:.1f}s")
        
        return {"filename": filename, "record_count": len(data_list), "duration": duration}
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    result = export_to_json_with_metadata(resource="users")
    print(f"Resultado: {result}")