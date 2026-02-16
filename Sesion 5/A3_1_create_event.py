import logging
from datetime import datetime, timedelta
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Calendars.ReadWrite permite crear/modificar eventos
SCOPES = ["Calendars.ReadWrite"]

def create_event(
    subject: str,
    start_time: str,  # ISO format: "2025-02-15T10:00:00"
    end_time: str,
    time_zone: str = "Europe/Madrid",
    location: str = None,
    attendees: list = None,
    is_online_meeting: bool = False,
):
    """Crear evento simple."""
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_time,
            "timeZone": time_zone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": time_zone,
        },
        "isReminderOn": True,
        "reminderMinutesBeforeStart": 15,
    }
    
    if location:
        payload["location"] = {"displayName": location}
    
    if attendees:
        payload["attendees"] = [
            {
                "emailAddress": {
                    "address": addr,
                    "name": addr.split("@")[0],  # Usar parte antes de @
                },
                "type": "required",
            }
            for addr in attendees
        ]
    
    if is_online_meeting:
        payload["isOnlineMeeting"] = True
        payload["onlineMeetingProvider"] = "teamsForBusiness"
    
    logger.info(f"Creando evento: {subject}")
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/events",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.ok:
        event = resp.json()
        logger.info(f"✅ Evento creado: {event['id']}")
        logger.info(f"   URL Teams: {event.get('onlineMeeting', {}).get('joinUrl', 'N/A')}")
        return event
    else:
        logger.error(f"❌ Error: {resp.text}")
        return None

if __name__ == "__main__":
    create_event(
        subject="Team Meeting",
        start_time="2025-02-15T10:00:00",
        end_time="2025-02-15T11:00:00",
        time_zone="Europe/Madrid",
        location="Conference Room B",
        attendees=["test@cursograph.onmicrosoft.com", "test@cursograph.onmicrosoft.com", "pablo.donate@cursograph.onmicrosoft.com"],
        is_online_meeting=True,
    )