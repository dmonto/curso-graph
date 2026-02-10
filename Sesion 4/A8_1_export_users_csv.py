import os
import csv
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
EXPORT_USER = os.getenv("EXPORT_USER", "admin@contoso.com")  # quién exporta

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

def export_users_to_csv(filename: str = None, filter_enabled: bool = True):
    """Exportar usuarios a CSV con metadata."""
    token = get_app_token()
    headers = {"Authorization": f"Bearer {token}", "ConsistencyLevel": "eventual"}
    
    # Nombre de archivo con timestamp
    if not filename:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"users_export_{timestamp}.csv"
    
    # Parámetros Graph
    params = {
        "$select": "id,displayName,userPrincipalName,mail,accountEnabled,createdDateTime",
        "$orderby": "displayName",
        "$top": 100,
        "$count": "true"
    }
    if filter_enabled:
        params["$filter"] = "accountEnabled eq true"
    
    url = "https://graph.microsoft.com/v1.0/users"
    
    # Streaming: escribir mientras se pagina
    record_count = 0
    export_start = datetime.utcnow()
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    'id', 'displayName', 'userPrincipalName', 'mail',
                    'accountEnabled', 'createdDateTime'
                ]
            )
            writer.writeheader()
            
            # Iterar con paginación
            next_url = url
            while next_url:
                logger.info(f"Descargando página (URL: {next_url[:80]}...)")
                if record_count == 0:
                    resp = requests.get(next_url, headers=headers, params=params, timeout=15)
                else:
                    resp = requests.get(next_url, headers=headers, timeout=15)
                
                resp.raise_for_status()
                data = resp.json()
                
                # Escribir registros en esta página
                for user in data.get('value', []):
                    writer.writerow(user)
                    record_count += 1
                
                next_url = data.get('@odata.nextLink')
                logger.info(f"  {len(data.get('value', []))} usuarios en esta página. Total: {record_count}")
        
        export_end = datetime.utcnow()
        duration = (export_end - export_start).total_seconds()
        
        logger.info(f"✅ Exportación completada")
        logger.info(f"  Archivo: {filename}")
        logger.info(f"  Registros: {record_count}")
        logger.info(f"  Duración: {duration:.1f}s")
        
        return {"filename": filename, "record_count": record_count, "duration": duration}
    
    except Exception as e:
        logger.error(f"❌ Error durante exportación: {e}")
        raise

if __name__ == "__main__":
    result = export_users_to_csv()
    print(f"Resultado: {result}")