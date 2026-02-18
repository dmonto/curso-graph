import requests
import os
from dotenv import load_dotenv
from A0_1_get_token import get_apponly_token
from datetime import datetime, timedelta, timezone

load_dotenv()

def get_calendar_events(token, user_id=None, days_ahead=7):
    """Obtiene eventos del calendario de Outlook."""
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Calcular fechas
    now = datetime.now(timezone.utc)
    future = now + timedelta(days=days_ahead)
    
    now_str = now.isoformat().replace('+00:00', 'Z')
    future_str = future.isoformat().replace('+00:00', 'Z')
    
    # Filtrar por fecha
    filter_param = f"start ge '{now_str}' and start le '{future_str}'"
    
    endpoint = "/me/events" if user_id is None else f"/users/{user_id}/events"
    
    r = requests.get(
        f"https://graph.microsoft.com/v1.0{endpoint}",
        headers=headers,
        params={"$filter": filter_param},
        timeout=30
    )
    
    if r.status_code == 200:
        events = r.json().get("value", [])
        print(f"✓ {len(events)} eventos obtenidos")
        return events
    else:
        raise Exception(f"Error: {r.text}")


def get_event_details(token, event_id):
    """Obtiene detalles completos de un evento."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {token}"}
    
    r = requests.get(
        f"https://graph.microsoft.com/v1.0/me/events/{event_id}",
        headers=headers,
        timeout=30
    )
    
    if r.status_code == 200:
        event = r.json()
        return {
            "title": event.get("subject", ""),
            "description": event.get("bodyPreview", ""),
            "start": event.get("start", {}).get("dateTime"),
            "end": event.get("end", {}).get("dateTime"),
            "attendees": [a["emailAddress"]["address"] for a in event.get("attendees", [])],
            "organizer": event.get("organizer", {}).get("emailAddress", {}).get("address", "")
        }
    else:
        raise Exception(f"Error: {r.text}")
   
def create_task_from_event(token, plan_id, bucket_id, event):
    """Crea tarea Planner desde evento Outlook."""
    
    import requests
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Extraer información del evento
    title = f"Follow-up: {event['subject']}"
    description = f"Seguimiento de: {event['subject']}\n\nDetalles:\n{event.get('bodyPreview', '')}"
    due_date = event['end']['dateTime']  # Usar fecha fin como vencimiento
    
    payload = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": title,
        "description": description,
        "dueDateTime": due_date,
        "priority": 2
    }
    
    r = requests.post(
        "https://graph.microsoft.com/v1.0/planner/tasks",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if r.status_code == 201:
        task = r.json()
        print(f"✓ Tarea creada: {title}")
        return task
    else:
        raise Exception(f"Error: {r.text}")

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
bucket_id = os.getenv("BUCKET_ID") or input("Id de Bucket:")
event = get_calendar_events(token, days_ahead=7)[0]
task = create_task_from_event(token, plan_id, bucket_id, event)