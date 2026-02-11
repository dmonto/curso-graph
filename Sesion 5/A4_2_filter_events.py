import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Definir rango
start_date = datetime.now(timezone.utc)
end_date = start_date + timedelta(days=30)

# Formatear fechas para el filtro
start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

# Construir filtro OData
filter_query = (
    f"start/dateTime ge '{start_str}' and "
    f"start/dateTime lt '{end_str}'"
)

url = "https://graph.microsoft.com/v1.0/me/calendar/events"

params = {
    "$filter": filter_query,
    "$orderby": "start/dateTime",
    "$top": 50
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    events = response.json().get("value", [])
    print(f"Encontrados {len(events)} eventos")
else:
    print(f"Error: {response.status_code}")