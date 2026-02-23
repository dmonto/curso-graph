import requests
import uuid
import urllib
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()
def add_task_reference(access_token, task_id, reference_alias, reference_url, reference_type="Other"):
    """Agrega una referencia a una tarea (archivo, link, etc)."""
        
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener detalles de la tarea
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}")
    
    task_details = response.json()
    etag = response.headers.get("ETag")
    
    # Agregar referencia
    references = task_details.get("references", {})
    encoded_url = urllib.parse.quote(reference_url, safe='')

    references = {
    encoded_url:{
      "@odata.type": "microsoft.graph.plannerExternalReference",
      "alias": reference_alias,
      "previewPriority": " !",
      "type": reference_type
    }}
    
    # Actualizar
    headers_patch = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }

    response = requests.patch(
        f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
        headers=headers_patch,
        json=references,
        timeout=30
    )
    
    if response.status_code in [200, 204]:
        print(f"✓ Referencia agregada")
        return 
    else:
        print(references)
        raise Exception(f"Error: {response.text}")

# USO
token = get_apponly_token()
task_id = input("Task ID: ")

add_task_reference(
    token, task_id,
    "Documento Word",
    "https://onedrive.empresa.com/archivo.docx",
    "Other"
)