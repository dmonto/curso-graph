from datetime import datetime, timezone
from jinja2 import Template
import requests
from apscheduler.schedulers.background import BackgroundScheduler

class DailySummaryGenerator:
    """Genera resúmenes diarios personalizados."""
    
    def __init__(self, access_token, user_email):
        self.access_token = access_token
        self.user_email = user_email
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def get_today_events(self):
        """Obtiene reuniones de hoy."""
        today = datetime.now(timezone.utc).date()
        start = datetime(today.year, today.month, today.day, 0, 0, 0).isoformat() + "Z"
        end = datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + "Z"
        
        params = {
            "startDateTime": start,
            "endDateTime": end,
            "$select": "subject,start,end,isReminderOn,organizer",
            "$orderby": "start/dateTime"
        }
        
        url = "https://graph.microsoft.com/v1.0/me/calendarView"
        response = requests.get(url, headers=self.headers, params=params)
        
        return response.json().get("value", []) if response.status_code == 200 else []
    
    def get_overdue_tasks(self):
        """Obtiene tareas vencidas de Planner."""
        # Asumir que tenemos plan_id conocido
        # En producción, obtener desde configuración
        
        today = datetime.now(timezone.utc).date().isoformat()
        
        params = {
            "$filter": f"dueDateTime lt '{today}'",
            "$select": "title,dueDateTime,percentComplete,assignments"
        }
        
        url = "https://graph.microsoft.com/v1.0/me/planner/tasks"
        response = requests.get(url, headers=self.headers, params=params)
        
        return response.json().get("value", []) if response.status_code == 200 else []
    
    def get_unread_emails(self):
        """Obtiene correos importantes sin leer."""
        params = {
            "$filter": "isRead eq false and importance eq 'high'",
            "$select": "subject,from,receivedDateTime,bodyPreview",
            "$orderby": "receivedDateTime desc",
            "$top": 5
        }
        
        url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
        response = requests.get(url, headers=self.headers, params=params)
        
        return response.json().get("value", []) if response.status_code == 200 else []
    
    def generate_html_summary(self):
        """Genera HTML del resumen diario."""
        events = self.get_today_events()
        tasks = self.get_overdue_tasks()
        emails = self.get_unread_emails()
        
        # Template HTML
        template_str = """
        <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; background: #f5f5f5; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
                    h1 { color: #0078d4; border-bottom: 3px solid #0078d4; padding-bottom: 10px; }
                    h2 { color: #333; margin-top: 25px; font-size: 18px; }
                    .section { margin-bottom: 25px; }
                    .event-item, .task-item, .email-item { 
                        padding: 12px; 
                        border-left: 4px solid #0078d4; 
                        background: #f9f9f9; 
                        margin-bottom: 10px; 
                    }
                    .event-item { border-left-color: #107c10; }
                    .task-item { border-left-color: #ff8c00; }
                    .email-item { border-left-color: #0078d4; }
                    .time { color: #666; font-size: 12px; }
                    .empty { color: #999; font-style: italic; }
                    .footer { color: #666; font-size: 12px; text-align: center; margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Resumen Diario - {{ date }}</h1>
                    
                    <div class="section">
                        <h2>Reuniones de Hoy ({{ events_count }})</h2>
                        {% if events %}
                            {% for event in events %}
                                <div class="event-item">
                                    <b>{{ event.subject }}</b>
                                    <div class="time">{{ event.start_time }} - {{ event.end_time }}</div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="empty">Sin reuniones programadas hoy</p>
                        {% endif %}
                    </div>
                    
                    <div class="section">
                        <h2>Tareas Vencidas ({{ tasks_count }})</h2>
                        {% if tasks %}
                            {% for task in tasks %}
                                <div class="task-item">
                                    <b>{{ task.title }}</b>
                                    <div class="time">Vencida: {{ task.due_date }}</div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="empty">Sin tareas vencidas</p>
                        {% endif %}
                    </div>
                    
                    <div class="section">
                        <h2>Correos Importantes sin Leer ({{ emails_count }})</h2>
                        {% if emails %}
                            {% for email in emails %}
                                <div class="email-item">
                                    <b>{{ email.subject }}</b>
                                    <div class="time">De: {{ email.from_address }} | {{ email.received_date }}</div>
                                    <p>{{ email.preview }}</p>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="empty">Sin correos pendientes</p>
                        {% endif %}
                    </div>
                    
                    <div class="footer">
                        <p>Este resumen fue generado automáticamente a las {{ generation_time }}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Preparar datos
        template_data = {
            "date": datetime.now().strftime("%d de %B de %Y"),
            "events": [{
                "subject": e["subject"],
                "start_time": e["start"]["dateTime"].split("T")[1][:5],
                "end_time": e["end"]["dateTime"].split("T")[1][:5]
            } for e in events],
            "events_count": len(events),
            "tasks": [{
                "title": t["title"],
                "due_date": t.get("dueDateTime", "N/A")
            } for t in tasks],
            "tasks_count": len(tasks),
            "emails": [{
                "subject": em["subject"],
                "from_address": em["from"]["emailAddress"]["name"],
                "received_date": em["receivedDateTime"][:10],
                "preview": em["bodyPreview"][:100]
            } for em in emails],
            "emails_count": len(emails),
            "generation_time": datetime.now().strftime("%H:%M:%S")
        }
        
        template = Template(template_str)
        return template.render(**template_data)
    
    def send_summary(self):
        """Envía el resumen diario por email."""
        html_content = self.generate_html_summary()
        
        payload = {
            "message": {
                "subject": f"Tu Resumen Diario - {datetime.now().strftime('%d %B %Y')}",
                "body": {
                    "contentType": "HTML",
                    "content": html_content
                },
                "toRecipients": [
                    {"emailAddress": {"address": self.user_email}}
                ]
            },
            "saveToSentItems": True
        }
        
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 202:
            print("✓ Resumen diario enviado")
            return True
        else:
            print(f"✗ Error enviando resumen: {response.status_code}")
            return False

# Uso con scheduler
def schedule_daily_summary(access_token, user_email, hour=8, minute=0):
    """Programa el resumen diario."""
    
    summary = DailySummaryGenerator(access_token, user_email)
    scheduler = BackgroundScheduler()
    
    # Ejecutar cada día a la hora especificada
    scheduler.add_job(
        func=summary.send_summary,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_summary"
    )
    
    scheduler.start()
    print(f"✓ Resumen diario programado para las {hour:02d}:{minute:02d}")