import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

def get_recurring_event_instances(access_token, event_id, start_date, end_date):
    """
    Obtiene las instancias de un evento recurrente dentro de un rango.
    """
   
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    params = {
        "startDateTime": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "endDateTime": end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    
    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}/instances"
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        
        return response.json().get("value", [])
    else:
        print(response.json())
        return []

# Uso
start = datetime.now(timezone.utc)
end = start + timedelta(days=30)

instances = get_recurring_event_instances(token, "AQMkAGZhYjEyMzRlLTg3ZWUALTQ3Y2YtYmVmMi1jMmJjOGEzZDNiODEARgAAA36WVQUwIBNMgqNGWhZuIDMHAKwVWMEnomVFsrEp96myWR8AAAIBDQAAAKwVWMEnomVFsrEp96myWR8AAAI4gQAAAA==", start, end)
for instance in instances:
    print(f"Instancia: {instance['subject']} en {instance['start']['dateTime']}")