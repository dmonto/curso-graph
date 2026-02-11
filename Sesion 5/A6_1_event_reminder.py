from datetime import datetime, timedelta, timezone
import schedule
import time
import requests
from A0_1_get_token import get_delegated_token

class EventReminder:
    """Sistema automático de recordatorios de eventos."""
    
    def __init__(self, access_token, user_email):
        self.access_token = access_token
        self.user_email = user_email
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def get_upcoming_events(self, minutes_ahead=40):
        """Obtiene eventos en los próximos N minutos."""
        now = datetime.now(timezone.utc)
        future = now + timedelta(minutes=minutes_ahead)
        
        params = {
            "startDateTime": now.isoformat() + "Z",
            "endDateTime": future.isoformat() + "Z",
            "$select": "subject,start,end,attendees,onlineMeetingUrl,organizer",
            "$orderby": "start/dateTime"
        }
        
        url = "https://graph.microsoft.com/v1.0/me/calendarView"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json().get("value", [])
        else:
            print(f"Error: {response.status_code}")
            return []
    
    def should_send_reminder(self, event):
        """Verifica si debe enviar recordatorio (30 min antes)."""
        event_time = datetime.fromisoformat(
            event["start"]["dateTime"].replace("Z", "+00:00")
        )
        now = datetime.utcnow().replace(tzinfo=event_time.tzinfo)
        
        minutes_until = (event_time - now).total_seconds() / 60
        
        # Enviar recordatorio entre 31 y 29 minutos antes
        return 29 <= minutes_until <= 31
    
    def send_reminder_email(self, event):
        """Envía email de recordatorio del evento."""
        event_time = event["start"]["dateTime"]
        subject = event["subject"]
        organizer = event.get("organizer", {}).get("emailAddress", {}).get("name", "Unknown")
        attendees_count = len(event.get("attendees", []))
        meeting_url = event.get("onlineMeetingUrl", "No disponible")
        
        # Generar HTML del email
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Recordatorio de Reunión</h2>
                <p><b>Título:</b> {subject}</p>
                <p><b>Hora:</b> {event_time}</p>
                <p><b>Organizador:</b> {organizer}</p>
                <p><b>Asistentes:</b> {attendees_count}</p>
                <hr>
                <p><b>Enlace de reunión:</b> <a href="{meeting_url}">{meeting_url}</a></p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    Este es un recordatorio automático de su sistema de automatización.
                </p>
            </body>
        </html>
        """
        
        payload = {
            "message": {
                "subject": f"Recordatorio: {subject} en 30 minutos",
                "body": {
                    "contentType": "HTML",
                    "content": html_body
                },
                "toRecipients": [
                    {"emailAddress": {"address": self.user_email}}
                ]
            },
            "saveToSentItems": True
        }
        
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        response = requests.post(url, headers=self.headers, json=payload)
        
        return response.status_code == 202
    
    def process_reminders(self):
        """Procesa todos los recordatorios pendientes."""
        events = self.get_upcoming_events()
        
        print(f"Verificando {len(events)} eventos próximos...")
        
        sent_count = 0
        for event in events:
            if self.should_send_reminder(event):
                subject = event["subject"]
                if self.send_reminder_email(event):
                    print(f"✓ Recordatorio enviado: {subject}")
                    sent_count += 1
                else:
                    print(f"✗ Error enviando recordatorio: {subject}")
        
        return sent_count

if __name__ == "__main__":
    SCOPES = ["Mail.ReadWrite"]
    token = get_delegated_token(SCOPES)

    # Uso
    reminder = EventReminder(token, "user@empresa.com")

    # Ejecutar cada 5 minutos
    schedule.every(5).minutes.do(reminder.process_reminders)

    while True:
        schedule.run_pending()
        time.sleep(60)