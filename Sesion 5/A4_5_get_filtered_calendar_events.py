import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_filtered_calendar_events(access_token, filters):
    """
    Obtiene eventos con filtros OData complejos.
    
    Args:
        filters: Diccionario con criterios de filtrado
    
    Example:
        filters = {
            'start_date': '2025-01-01T00:00:00Z',
            'end_date': '2025-01-31T23:59:59Z',
            'category': 'Trabajo',
            'is_reminder_on': True
        }
    """
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Construir filtro base por fechas
    filter_parts = []
    
    if 'start_date' in filters and 'end_date' in filters:
        filter_parts.append(
            f"start/dateTime ge '{filters['start_date']}' and "
            f"start/dateTime lt '{filters['end_date']}'"
        )
    
    if 'category' in filters:
        filter_parts.append(f"categories/any(c:c eq '{filters['category']}')")
    
    if 'is_reminder_on' in filters:
        reminder_value = str(filters['is_reminder_on']).lower()
        filter_parts.append(f"isReminderOn eq {reminder_value}")
    
    if 'subject_contains' in filters:
        filter_parts.append(
            f"startsWith(subject, '{filters['subject_contains']}')"
        )
    
    filter_query = " and ".join(filter_parts)
    
    params = {
        "$filter": filter_query,
        "$select": "subject,start,end,categories,isReminderOn",
        "$orderby": "start/dateTime"
    }
    
    url = "https://graph.microsoft.com/v1.0/me/calendar/events"
    response = requests.get(url, headers=headers, params=params)
    
    return response.json().get("value", []) if response.status_code == 200 else []

# Uso
filters = {
    'start_date': '2025-01-01T00:00:00Z',
    'end_date': '2026-03-01T23:59:59Z',
    'is_reminder_on': True
}

events = get_filtered_calendar_events(token, filters)