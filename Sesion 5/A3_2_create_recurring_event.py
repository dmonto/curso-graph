import logging
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Calendars.ReadWrite"]

def create_recurring_event(
    subject: str,
    start_date: str,  # "2025-02-17"
    start_time: str,  # "09:00:00"
    end_time: str,    # "10:00:00"
    time_zone: str,
    days_of_week: list,  # ["monday", "tuesday", ...]
    end_date: str,  # "2025-12-31" o None para infinito
):
    """Crear evento recurrente."""
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construir datetime
    start_datetime = f"{start_date}T{start_time}"
    end_datetime = f"{start_date}T{end_time}"
    
    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_datetime,
            "timeZone": time_zone,
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": time_zone,
        },
        "recurrence": {
            "pattern": {
                "type": "weekly",
                "interval": 1,
                "daysOfWeek": days_of_week,
                "firstDayOfWeek": "sunday",
            },
            "range": {
                "type": "endDate" if end_date else "noEnd",
                "startDate": start_date,
                "endDate": end_date,
                "recurrenceTimeZone": time_zone,
            },
        },
        "isReminderOn": True,
        "reminderMinutesBeforeStart": 10,
    }
    
    logger.info(f"Creando evento recurrente: {subject}")
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/events",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.ok:
        event = resp.json()
        logger.info(f"✅ Evento recurrente creado: {event['id']}")
        logger.info(f"   Patrón: {', '.join(days_of_week)} de {start_date} hasta {end_date or 'sin fin'}")
        return event
    else:
        logger.error(f"❌ Error: {resp.text}")
        return None

if __name__ == "__main__":
    create_recurring_event(
        subject="Weekly Standup",
        start_date="2026-02-01",
        start_time="09:00:00",
        end_time="09:30:00",
        time_zone="Europe/Madrid",
        days_of_week=["monday", "tuesday", "wednesday", "thursday", "friday"],
        end_date="2026-02-28",
    )