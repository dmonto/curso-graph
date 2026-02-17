import requests
import os
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv

load_dotenv()

def format_graph_datetime(dt):
    """Graph DateTimeOffset: yyyy-MM-ddTHH:mm:ssZ (sin micros/offset)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def search_with_filters(access_token, drive_id, name_contains=None, file_type=None, 
                        size_min=None, size_max=None, top=50):
    """Búsqueda avanzada con filtros."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Construir filtro
    filters = []
    
    if name_contains:
        filters.append(f"startswith(name, '{name_contains}')")
    
    if file_type:  # ej: "docx"
        filters.append(f"endswith(name, '.{file_type}')")
       
    if size_min is not None:
        filters.append(f"size ge {size_min}")
    
    if size_max is not None:
        filters.append(f"size le {size_max}")
    
    filter_string = " and ".join(filters) if filters else None
    
    params = {"$top": top}
    if filter_string:
        params["$filter"] = filter_string
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children",
        headers=headers,
        params=params,
        timeout=30
    )
    print(response.json())
    
    if response.status_code == 200:
        items = response.json().get("value", [])
        return items
    
    return []

# USO


token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
results = search_with_filters(
    token,
    drive_id,
    name_contains="sesion",
    file_type="md"
)

print(f"Encontrados: {len(results)}")