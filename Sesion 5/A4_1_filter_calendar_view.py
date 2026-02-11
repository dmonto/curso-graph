import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

# Configuración
SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Definir rango de fechas (próximos 7 días)
start_date = datetime.now(timezone.utc)
end_date = start_date + timedelta(days=7)

# Formatear en ISO 8601 UTC
start_datetime = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
end_datetime = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

# URL del endpoint
url = "https://graph.microsoft.com/v1.0/me/calendarView"

# Parámetros de la consulta
params = {
    "startDateTime": start_datetime,
    "endDateTime": end_datetime,
    "$top": 25,  # Paginación
    "$orderby": "start/dateTime"  # Ordenar por fecha
}

# Realizar solicitud
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    events = response.json().get("value", [])
    for event in events:
        print(f"Título: {event['subject']}")
        print(f"Inicio: {event['start']['dateTime']}")
        print(f"Fin: {event['end']['dateTime']}")
        print("---")
else:
    print(f"Error: {response.status_code}")
    print(response.json())