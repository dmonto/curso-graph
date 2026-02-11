import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_calendar_events_with_recurring(access_token, days_ahead=7):
    """
    Obtiene eventos incluidos los recurrentes en el rango especificado.
    calendarView maneja automáticamente la expansión de eventos recurrentes.
    """    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": "outlook.timezone=\"Europe/Madrid\""
    }
    
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=days_ahead)
    
    params = {
        "startDateTime": start.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "endDateTime": end.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "$select": "subject,start,end,iCalUId,type,isReminderOn,reminderMinutesBeforeStart",
        "$orderby": "start/dateTime"
    }
    
    url = "https://graph.microsoft.com/v1.0/me/calendarView"
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Uso
events = get_calendar_events_with_recurring(token, days_ahead=14)

for event in events:
    print(f"Evento: {event['subject']}")
    print(f"Tipo: {event['type']}")  # singleInstance, occurrence, exception, seriesMaster
    print(f"Inicio: {event['start']['dateTime']}")