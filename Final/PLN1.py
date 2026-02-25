"""
================================================================================
SISTEMA DE GESTIÓN: SHAREPOINT A PLANNER CON TRAZA DETALLADA EN DRIVE
================================================================================
DESCRIPCIÓN TÉCNICA:
1. AUTENTICACIÓN: MSAL (App-Only) contra Microsoft Graph.
2. LOGGING REMOTO: Gestiona 'sp2planner.log' en el Drive de origen.
   - Registra ficheros detectados.
   - Registra cada tarea creada (Título e ID).
   - Captura y registra errores de formato o de API.
3. PROCESAMIENTO: Una tarea en Planner por cada fila del CSV.
4. ARCHIVADO: Mueve el CSV procesado a /backup con sufijo '_proc.csv'.
================================================================================
"""

import requests
import pandas as pd
import io
import os
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SITE_ID = os.getenv("SITE_ID")
DRIVE_ID = os.getenv("DRIVE_ID")
PLAN_ID = os.getenv("PLAN_ID")

class RemoteLogger:
    """Gestiona la lectura y escritura del log directamente en SharePoint."""
    def __init__(self, headers):
        self.headers = headers
        self.log_name = "sp2planner.log"
        self.entries = []
        self.log_id = self._get_log_id()

    def _get_log_id(self):
        url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children?$filter=name eq '{self.log_name}'"
        res = requests.get(url, headers=self.headers).json()
        items = res.get('value', [])
        return items[0]['id'] if items else None

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        self.entries.append(line)

    def save_to_drive(self):
        """Descarga el log actual, concatena la nueva traza y lo sube."""
        current_content = ""
        if self.log_id:
            download_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/items/{self.log_id}/content"
            res = requests.get(download_url, headers=self.headers)
            if res.status_code == 200:
                current_content = res.text + "\n"
        
        full_log = current_content + "\n".join(self.entries)
        upload_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{self.log_name}:/content"
        requests.put(upload_url, headers=self.headers, data=full_log.encode('utf-8'))

def get_token():
    app = ConfidentialClientApplication(CLIENT_ID, client_credential=CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}")
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    raise RuntimeError("Error crítico: No se pudo obtener el token de acceso.")

def map_priority(prioridad_texto):
    p = str(prioridad_texto).strip().lower()
    if 'alta' in p or 'urgente' in p: return 3
    if 'baja' in p: return 9
    return 5

def format_date(fecha_str):
    try:
        dt = datetime.strptime(str(fecha_str).strip(), "%d/%m/%Y")
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except: return None

def get_bucket_id(headers, plan_id, bucket_name="Pendiente"):
    url = f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets"
    res = requests.get(url, headers=headers).json()
    for bucket in res.get('value', []):
        if bucket['name'].lower() == bucket_name.lower(): return bucket['id']
    return None

def get_or_create_backup_folder(headers, logger):
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children"
    res = requests.get(url, headers=headers).json()
    for item in res.get('value', []):
        if item['name'] == 'backup' and 'folder' in item: return item['id']
    
    logger.log("SISTEMA: Creando carpeta de backup inexistente.")
    payload = {"name": "backup", "folder": {}}
    return requests.post(url, headers=headers, json=payload).json()['id']

def process_file_rows(headers, item, backup_id, bucket_id, logger):
    nombre_archivo = item['name']
    nuevo_nombre = nombre_archivo.lower().replace(".csv", "_proc.csv")
    logger.log(f"FICHERO: Detectado '{nombre_archivo}'. Iniciando lectura...")

    try:
        # Descarga de contenido
        content = requests.get(item.get('@microsoft.graph.downloadUrl')).content
        
        # Intento de lectura con detección de encoding
        try:
            df = pd.read_csv(io.BytesIO(content), sep=None, engine='python', encoding='utf-8-sig')
        except Exception:
            df = pd.read_csv(io.BytesIO(content), sep=None, engine='python', encoding='latin-1')

        if df.empty:
            logger.log(f"ADVERTENCIA: El archivo '{nombre_archivo}' está vacío.")
            return

        # Procesamiento fila a fila
        for index, row in df.iterrows():
            try:
                titulo = f"{row['Tarea']} - {row['Detalle']}"
                task_payload = {
                    "planId": PLAN_ID,
                    "bucketId": bucket_id,
                    "title": titulo,
                    "priority": map_priority(row['Prioridad']),
                    "dueDateTime": format_date(row['Fecha'])
                }
                
                t_res = requests.post("https://graph.microsoft.com/v1.0/planner/tasks", headers=headers, json=task_payload)
                
                if t_res.status_code == 201:
                    task_id = t_res.json()['id']
                    logger.log(f"  [OK] Tarea creada: {row['Tarea']} | ID: {task_id}")
                    
                    # Detalles adicionales
                    detail_payload = {"description": f"Fila: {index+1}\nDetalle: {row['Detalle']}\nPrioridad: {row['Prioridad']}"}
                    requests.patch(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
                                   headers={**headers, "If-Match": t_res.headers['ETag']}, json=detail_payload)
                else:
                    logger.log(f"  [ERROR] No se pudo crear tarea para fila {index+1}: {t_res.text}")

            except KeyError as e:
                logger.log(f"  [ERROR] Columna faltante en fila {index+1}: {str(e)}")
            except Exception as e:
                logger.log(f"  [ERROR] Inesperado en fila {index+1}: {str(e)}")

        # Movimiento final del archivo
        move_payload = {"parentReference": {"id": backup_id}, "name": nuevo_nombre}
        m_res = requests.patch(f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/items/{item['id']}", 
                               headers=headers, json=move_payload)
        
        if m_res.status_code == 200:
            logger.log(f"FICHERO: '{nombre_archivo}' movido a /backup correctamente.")
        else:
            logger.log(f"ERROR: No se pudo mover '{nombre_archivo}' tras procesarlo.")

    except Exception as e:
        logger.log(f"ERROR CRÍTICO procesando contenido de '{nombre_archivo}': {str(e)}")

def main():
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        logger = RemoteLogger(headers)
        logger.log(">>> INICIO DE SESIÓN DE AUTOMATIZACIÓN <<<")

        bucket_id = get_bucket_id(headers, PLAN_ID, "Pendiente")
        if not bucket_id:
            logger.log("ADVERTENCIA: Bucket 'Pendiente' no encontrado. Usando bucket predeterminado.")

        backup_id = get_or_create_backup_folder(headers, logger)

        # Listar raíz del Drive
        list_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children"
        items = requests.get(list_url, headers=headers).json().get('value', [])

        csv_encontrados = False
        for item in items:
            # Filtro: Solo archivos CSV que no tengan el sufijo de procesado
            if "file" in item and item['name'].lower().endswith('.csv') and "_proc.csv" not in item['name'].lower():
                csv_encontrados = True
                process_file_rows(headers, item, backup_id, bucket_id, logger)

        if not csv_encontrados:
            logger.log("SISTEMA: No hay archivos .csv pendientes en la raíz.")

        logger.log(">>> FIN DE SESIÓN DE AUTOMATIZACIÓN <<<")
        logger.save_to_drive()

    except Exception as e:
        print(f"Error fatal en el flujo principal: {e}")

if __name__ == "__main__":
    main()