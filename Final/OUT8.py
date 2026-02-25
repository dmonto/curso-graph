import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from msal import PublicClientApplication
import os
from dateutil import parser  
import json


def get_delegated_token(scopes, refresh_if_needed: bool = True):
    """Obtener token delegado (usuario presente)."""
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    
    # Usar device code flow para interactividad
    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    
    return result["access_token"]



def get_calendar_events_with_timezone(access_token, tz="Europe/Madrid", days=7):
    """
    Obtiene eventos respetando zona horaria.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": f'outlook.timezone="{tz}"'  # Comillas dobles
    }
    
    now_utc = datetime.now(timezone.utc)
    start = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")  # 2026-02-11T10:50:00Z
    end_utc = now_utc + timedelta(days=days)
    end = end_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    params = {
        "$select": "subject,start,end,organizer",
        "$orderby": "start/dateTime"
    }
    
    url = f"https://graph.microsoft.com/v1.0/me/calendarView?startDateTime={start}&endDateTime={end}"
    # url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/events"
        
    print(f"🔍 Query: {url}")  # Debug
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        events = response.json().get("value", [])        
        return events
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return []


def get_todo_list_id(access_token, list_name="Tareas Calendario"):
    """Obtiene o crea lista To Do."""
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    # GET listas
    response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
    if response.status_code == 200:
        lists = response.json().get("value", [])
        for lst in lists:
            if lst["displayName"] == list_name:
                return lst["id"]
    
    # Crea nueva
    create_payload = {"displayName": list_name, "is_shared": False}
    response = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists", 
                            headers=headers, json=create_payload)
    if response.status_code == 201:
        print(f"✓ Lista creada: {list_name}")
        return response.json()["id"]
    return None


def create_todo_from_event(access_token, event, todo_list_id):
    """Crea task de seguimiento To Do desde evento del calendario."""
    
    # --- CUERPO DE LA TAREA (JSON) ---
    subject = event["subject"][:200]

    task_body = {        
        "title":f"📅 Seguimiento: {subject}",
        "body": {
            "contentType": "text",
            "content": event.get("bodyPreview", "")[:1500]
        },        
        "dueDateTime": {
            "dateTime": event["end"]["dateTime"],
            "timeZone": "UTC"
        }
    }

    # --- CABECERAS ---
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # --- SOLICITUD POST ---
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{todo_list_id}/tasks"
    response = requests.post(url, headers=headers, json=task_body)

    # --- MANEJO DE RESPUESTA ---
    if response.status_code == 201:
        print("Tarea creada exitosamente:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error al crear la tarea: {response.status_code}")
        print(response.text)




if __name__ == "__main__":
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED")
    TENANT_ID = os.getenv("TENANT_ID")
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    GROUP_ID = os.getenv("GROUP_ID")
    SCOPES = ["Calendars.Read"]

    # Conectamos con delegada porque no logramos que funcione con APPONLY
    token = get_delegated_token(SCOPES)

    # Obtenemos los eventos de los próximos 7 días
    events = get_calendar_events_with_timezone(token, tz="Europe/Madrid", days=7)
    for event in events:
            print(f"📅 {event['subject']}")
            print(f"  Inicio: {event['start']['dateTime']} ({event['start']['timeZone']})")
            print(f"  Fin: {event['end']['dateTime']} ({event['end']['timeZone']})")
            print(f"  Organizador: {event.get('organizer', {}).get('emailAddress', {}).get('name', 'N/A')}")
            print("---")
    
    # Creamos o generamos la lista TO-DO
    todo_list_id = get_todo_list_id(token)
    print("Id To-do:", todo_list_id)

    # Creamos los to-do en la lista
    for event in events:
        create_todo_from_event(token, event, todo_list_id)

