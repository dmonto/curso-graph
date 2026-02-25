from msal import ConfidentialClientApplication
import os
import time
from dotenv import load_dotenv
 
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # permisos de aplicación
 
 
GRAPH_V1 = "https://graph.microsoft.com/v1.0"
 
def _headers() -> dict:
    return {
        "Authorization": f"Bearer {get_apponly_token()}",
        "Content-Type": "application/json"
    }
 
 
def get_apponly_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Error en autenticación app-only: {result.get('error_description')}")
    return result["access_token"]
 
import requests
 
load_dotenv()
 
def get_plan(access_token, plan_id):
    """Obtiene detalles de un plan."""
   
    import requests
   
    headers = {"Authorization": f"Bearer {access_token}"}
   
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/o26HB_beVEKhW11xBK8K05gAFeEW",
        headers=headers,
        timeout=30
    )
   
    if response.status_code == 200:
        plan = response.json()
        return {
            "id": plan.get("id"),
            "title": plan.get("title"),
            "owner": plan.get("owner"),
            "created": plan.get("createdDateTime"),
            "modified": plan.get("modifiedDateTime")
        }
    else:
        raise Exception(f"Error: {response.text}")
 
# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
plan_info = get_plan(token, plan_id)
print(plan_info)
 
 
load_dotenv()
 
def list_plan_buckets(access_token, plan_id):
    """Lista todos los buckets de un plan."""
       
    headers = {"Authorization": f"Bearer {access_token}"}
   
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets",
        headers=headers,
        timeout=30
    )
   
    if response.status_code == 200:
        buckets = response.json().get("value", [])
       
        result = []
        for bucket in buckets:
            result.append({
                "id": bucket.get("id"),
                "name": bucket.get("name"),
                "planId": bucket.get("planId")
            })
       
        print(f"✓ {len(result)} buckets encontrados")
        return result
    else:
        raise Exception(f"Error: {response.text}")
 
# USO
if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
    buckets = list_plan_buckets(token, plan_id)
    for bucket in buckets:
        print(f"  {bucket['name']}: {bucket['id']}")
 
 
 
load_dotenv()
 
def list_bucket_tasks(access_token, bucket_id):
    """Lista todas las tareas de un bucket."""
   
    import requests
   
    headers = {"Authorization": f"Bearer {access_token}"}
   
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/buckets/{bucket_id}/tasks",
        headers=headers,
        timeout=30
    )
   
    if response.status_code == 200:
        tasks = response.json().get("value", [])
       
        result = []
        for task in tasks:
            result.append({
                "id": task.get("id"),
                "title": task.get("title"),
                "status": task.get("status"),
                "priority": task.get("priority"),
                "percentComplete": task.get("percentComplete"),
                "dueDate": task.get("dueDateTime")
            })
       
        print(f"✓ {len(result)} tareas encontradas")
        return result
    else:
        raise Exception(f"Error: {response.text}")
 
 
 
def get_group_id(group_name: str) -> str:
    """
    Busca un M365 Group por displayName usando $filter.
    Requiere permiso de aplicación: Group.Read.All
    """
    url = f"{GRAPH_V1}/groups"
    params = {
        "$filter": f"displayName eq '{group_name}'",
        "$select": "id,displayName"
    }
    response = requests.get(url, headers=_headers(), params=params)
    response.raise_for_status()
 
    groups = response.json().get("value", [])
    if not groups:
        raise ValueError(f"No se encontró ningún grupo llamado '{group_name}'")
 
    group = groups[0]
    print(f"[✓] Grupo encontrado: '{group['displayName']}' → ID: {group['id']}")
    return group["id"]
 
 
def get_disco_id(group_id: str) -> str:
    """Obtiene el ID de la biblioteca de documentos (Drive) del grupo."""
    url = f"{GRAPH_V1}/groups/{group_id}/drive"
    resp = requests.get(url, headers=_headers())
    resp.raise_for_status()
    return resp.json()["id"]
 
def crea_carpeta(drive_id: str, folder_name: str) -> str:
    """Crea una carpeta si no existe. Devuelve el folder_id."""
    # 1. Intentar crear. Si ya existe, Graph puede devolver error o conflicto según config.
    # Usaremos 'conflictBehavior': 'fail' para detectar si existe y buscarlo, o 'replace' (cuidado).
    # Mejor: Listar/Buscar primero para ser idempotente.
   
    # Buscamos si existe
    url_search = f"{GRAPH_V1}/drives/{drive_id}/root/children?$filter=name eq '{folder_name}'"
    resp = requests.get(url_search, headers=_headers())
    resp.raise_for_status()
    items = resp.json().get("value", [])
   
    if items:
        print(f"  [i] La carpeta '{folder_name}' ya existe. Usando la existente.")
        return items[0]["id"]
 
    # Si no existe, creamos
    url_create = f"{GRAPH_V1}/drives/{drive_id}/root/children"
    body = {
        "name": folder_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "fail"
    }
    resp = requests.post(url_create, headers=_headers(), json=body)
    resp.raise_for_status()
    print(f"  [✓] Carpeta creada: '{folder_name}'")
    return resp.json()["id"]
 
 
def sube_fichero(drive_id: str, folder_id: str, filename: str, content: str):
    """Sube un archivo de texto a la carpeta especificada."""
    # PUT /drives/{drive-id}/items/{parent-id}:/{filename}:/content
    url = f"{GRAPH_V1}/drives/{drive_id}/items/{folder_id}:/{filename}:/content"
   
    # Headers para texto plano
    headers = _headers()
    headers["Content-Type"] = "text/plain"
   
    resp = requests.put(url, headers=headers, data=content.encode('utf-8'))
    resp.raise_for_status()
    print(f"  [✓] Archivo '{filename}' subido correctamente.")
    return resp.json().get("webUrl") # Enlace directo al archivo
 
 
 
def _is_team_provisioned(group_id: str) -> bool:
    """Comprueba si el grupo M365 tiene Teams provisionado."""
    url = f"{GRAPH_V1}/groups/{group_id}?$select=resourceProvisioningOptions"
    resp = requests.get(url, headers=_headers())
    resp.raise_for_status()
    options = resp.json().get("resourceProvisioningOptions", [])
    return "Team" in options
 
def _provision_team(group_id: str) -> None:
    """
    Convierte un grupo M365 existente en un Team.
    Requiere que el grupo tenga al menos 1 owner.
    Puede tardar hasta 30s en propagarse.
    """
    url = f"{GRAPH_V1}/teams"
    body = {
        "template@odata.bind": "https://graph.microsoft.com/v1.0/teamsTemplates('standard')",
        "group@odata.bind": f"https://graph.microsoft.com/v1.0/groups/{group_id}"
    }
    resp = requests.post(url, headers=_headers(), json=body)
 
    if resp.status_code == 202:  # Accepted — es asíncrono
        print(f"  [i] Teams provisionado para el grupo. Esperando propagación...")
        time.sleep(30)  # Graph tarda ~20-30s en activarlo
    else:
        resp.raise_for_status()
 
def create_channel(team_id: str, channel_name: str) -> str:
   
    """
    Crea un canal estándar. Verifica y provisiona Teams si hace falta.
    """
    # 1. Comprobar si el grupo tiene Teams
    if not _is_team_provisioned(team_id):
        print(f"  [!] El grupo no tiene Teams. Provisionando...")
        _provision_team(team_id)
 
   
    """Crea un canal estándar en el Team."""
    # 1. Comprobar si existe
    url_list = f"{GRAPH_V1}/teams/{team_id}/channels?$filter=displayName eq '{channel_name}'"
    resp = requests.get(url_list, headers=_headers())
    # Ojo: $filter en channels a veces es limitado. Iteramos si falla el filtro.
    if resp.status_code == 200:
        channels = resp.json().get("value", [])
        for ch in channels:
            if ch["displayName"].lower() == channel_name.lower():
                print(f"  [i] El canal '{channel_name}' ya existe.")
                return ch["id"]
   
    # 2. Crear si no existe
    url_create = f"{GRAPH_V1}/teams/{team_id}/channels"
    body = {
        "displayName": channel_name,
        "description": f"Canal generado automáticamente para la tarea {channel_name}",
        "membershipType": "standard"
    }
    resp = requests.post(url_create, headers=_headers(), json=body)
    resp.raise_for_status()
    print(f"  [✓] Canal creado: '{channel_name}'")
    return resp.json()["id"]
 
 
 
def procesa_tareas(task_title: str):
   
    group_id = get_group_id("Plandeprueba")
    drive_id = get_disco_id(group_id)
    folder_id = crea_carpeta(drive_id, task_title)
 
    contenido_readme = (
        f"Bienvenido al espacio de trabajo para la tarea: {task_title}.\n\n"
        "Este directorio y el canal de Teams han sido generados automáticamente.\n"
        "Por favor, sube aquí toda la documentación técnica."
    )
 
    file_link = sube_fichero(drive_id, folder_id, "README_BIENVENIDA.txt", contenido_readme)
   
    #crea el canal de teams
    safe_channel_name = "".join(c for c in task_title if c.isalnum() or c in " -_")[:50]
    channel_id = create_channel(team_id=group_id, channel_name=safe_channel_name)
   
    # PASO 5 (Alternativo): Mensaje de bienvenida
    # Como enviar mensaje es 'Protected API', imprimimos lo que haríamos o
    # creamos un aviso en consola. El README ya contiene el link.
    print(f"  [i] Recursos listos. Link carpeta: {file_link}")
 
 
# USO
if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
    buckets = list_plan_buckets(token, plan_id)
    for bucket in buckets:
        print(f"  {bucket['name']}: {bucket['id']}")
       
    bucket_id = os.getenv("BUCKET_ID") or input("ID de Bucket: ")
    tasks = list_bucket_tasks(token, bucket_id)
    for task in tasks:
        print(f"  {task['title']}: {task['status']} ({task['percentComplete']}%) - {task['id']}")
        procesa_tareas(task['title'])
