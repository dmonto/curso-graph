import logging
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Calendars.ReadWrite"]

def update_event(token: str, event_id: str, **changes):
    """Actualizar evento (cambios parciales)."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = changes
    
    logger.info(f"Actualizando evento {event_id}...")
    
    resp = requests.patch(
        f"https://graph.microsoft.com/v1.0/me/events/{event_id}",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.ok:
        logger.info(f"✅ Evento actualizado")
        return resp.json()
    else:
        logger.error(f"❌ Error: {resp.text}")
        return None

def cancel_event(token: str, event_id: str, comment: str = None):
    """Cancelar evento."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {}
    if comment:
        payload["comment"] = comment
    
    logger.info(f"Cancelando evento {event_id}...")
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/events/{event_id}/cancel",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.status_code == 200:
        logger.info(f"✅ Evento cancelado")
        return True
    else:
        logger.error(f"❌ Error: {resp.text}")
        return False

def list_upcoming_events(token: str, days_ahead: int = 7):
    """Listar próximos eventos."""
    headers = {"Authorization": f"Bearer {token}"}
    
    from datetime import datetime, timedelta
    
    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"
    
    params = {
        "startDateTime": start,
        "endDateTime": end,
        "$select": "subject,start,end,organizer,attendees",
        "$orderby": "start/dateTime",
        "$top": 20,
    }
    
    logger.info(f"Listando eventos próximos {days_ahead} días...")
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/calendarview",
        headers=headers,
        params=params,
        timeout=15,
    )
    
    if resp.ok:
        events = resp.json().get("value", [])
        logger.info(f"✅ {len(events)} eventos encontrados")
        
        for event in events:
            print(f"\n{event['subject']}")
            print(f"  Inicio: {event['start']['dateTime']}")
            print(f"  Fin: {event['end']['dateTime']}")
            print(f"  Organizador: {event['organizer']['emailAddress']['name']}")
            print(f"  Asistentes: {len(event.get('attendees', []))}")
        
        return events
    else:
        logger.error(f"❌ Error: {resp.text}")
        return []

if __name__ == "__main__":
    token = get_delegated_token(SCOPES)
    
    # Listar próximos eventos
    events = list_upcoming_events(token, days_ahead=14)
    
    if events:
        # Actualizar el primero
        event_id = events[0]['id']
        update_event(token, event_id, subject=f"{events[0]['subject']} (UPDATED)")
        
        # Cancelar (comentado por seguridad)
        # cancel_event(token, event_id, comment="Cambio de planes")