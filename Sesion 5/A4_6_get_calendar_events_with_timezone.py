import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

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
    
    print(f"🔍 Query: {url}")  # Debug
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        events = response.json().get("value", [])
        for event in events:
            print(f"📅 {event['subject']}")
            print(f"  Inicio: {event['start']['dateTime']} ({event['start']['timeZone']})")
            print(f"  Fin: {event['end']['dateTime']} ({event['end']['timeZone']})")
            print(f"  Organizador: {event.get('organizer', {}).get('emailAddress', {}).get('name', 'N/A')}")
            print("---")
        return events
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return []

# Test
get_calendar_events_with_timezone(token, tz="Europe/Madrid", days=7)
