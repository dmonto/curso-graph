from typing import List, Dict
import requests
from datetime import datetime, timedelta, timezone
from A0_1_get_token import get_delegated_token

SCOPES = ["Calendars.Read"]
token = get_delegated_token(SCOPES)

class CalendarView:
    """
    Gestor de vistas de calendario para Microsoft 365.
    """
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Prefer": "outlook.timezone=\"Europe/Madrid\""
        }
    
    def get_week_view(self, start_date: datetime = None) -> List[Dict]:
        """Obtiene la vista de una semana."""
        if start_date is None:
            start_date = datetime.now(timezone.utc)
        
        end_date = start_date + timedelta(days=7)
        return self._get_events_in_range(start_date, end_date)
    
    def get_month_view(self, year: int, month: int) -> List[Dict]:
        """Obtiene la vista de un mes."""
        start_date = datetime(year, month, 1)
        
        # Calcular último día del mes
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        return self._get_events_in_range(start_date, end_date)
    
    def get_today_events(self) -> List[Dict]:
        """Obtiene los eventos de hoy."""
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        return self._get_events_in_range(today, tomorrow)
       
    def _get_events_in_range(self, start: datetime, end: datetime) -> List[Dict]:
        """Obtiene eventos en un rango de fechas."""
        params = {
            "startDateTime": start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "endDateTime": end.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "$select": "subject,start,end,categories,isReminderOn,organizer",
            "$orderby": "start/dateTime"
        }
        
        url = f"{self.base_url}/me/calendarView"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json().get("value", [])
        else:
            raise Exception(f"Error al obtener eventos: {response.status_code}")

# Uso del sistema
calendar = CalendarView(token)

# Vista semanal
week_events = calendar.get_week_view()
print(f"Eventos esta semana: {len(week_events)}")

# Vista mensual
month_events = calendar.get_month_view(2026, 2)
print(f"Eventos en febrero 2026: {len(month_events)}")

# Eventos de hoy
today_events = calendar.get_today_events()
for event in today_events:
    print(f"- {event['subject']} ({event['start']['dateTime']})")

# Estado de disponibilidad
start = datetime.now(timezone.utc)
end = start + timedelta(days=1)
events = calendar._get_events_in_range(start, end)
print(events)