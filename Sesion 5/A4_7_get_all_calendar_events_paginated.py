import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_all_calendar_events_paginated(access_token, start_date, end_date, page_size=25):
    """
    Obtiene todos los eventos con paginación automática.
    """
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    all_events = []
    skip_token = None
    
    while True:
        params = {
            "startDateTime": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "endDateTime": end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "$top": page_size,
            "$orderby": "start/dateTime"
        }
        
        # Si hay token de paginación, úsalo
        if skip_token:
            params["$skiptoken"] = skip_token
        
        url = "https://graph.microsoft.com/v1.0/me/calendarView"
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            break
        
        data = response.json()
        all_events.extend(data.get("value", []))
        
        # Comprobar si hay más páginas
        if "@odata.nextLink" in data:
            # Extraer skiptoken del nextLink
            skip_token = data["@odata.nextLink"].split("$skiptoken=")[1]
        else:
            break
    
    return all_events

# Uso
start = datetime.now(timezone.utc)
end = start + timedelta(days=30)

all_events = get_all_calendar_events_paginated(token, start, end, page_size=25)
print(f"Total de eventos obtenidos: {len(all_events)}")