import logging
import os
import schedule
import time
from dotenv import load_dotenv
from A0_1_get_token import get_delegated_token
from A6_2_daily_summary import DailySummaryGenerator
from A6_1_event_reminder import EventReminder

# Configuración
SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)
USER_EMAIL = os.getenv("USER_EMAIL")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomationEngine:
    """Motor central de automatización."""
    
    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.tasks = []
    
    def add_task(self, name, func, schedule_config):
        """Registra una tarea automática."""
        self.tasks.append({
            "name": name,
            "func": func,
            "schedule": schedule_config
        })
    
    def start(self):
        """Inicia el motor de automatización."""
        for task in self.tasks:
            name = task["name"]
            config = task["schedule"]
            
            if config["type"] == "interval":
                schedule.every(config["minutes"]).minutes.do(task["func"])
                logger.info(f"Tarea '{name}' programada cada {config['minutes']} minutos")
            
            elif config["type"] == "daily":
                schedule.every().day.at(config["time"]).do(task["func"])
                logger.info(f"Tarea '{name}' programada diariamente a las {config['time']}")
        
        logger.info("=== MOTOR DE AUTOMATIZACIÓN INICIADO ===")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Instanciar motor
engine = AutomationEngine(token, USER_EMAIL)

# Registrar tareas
reminder = EventReminder(token, USER_EMAIL)
engine.add_task(
    name="Recordatorios de eventos",
    func=reminder.process_reminders,
    schedule_config={"type": "interval", "minutes": 5}
)

summary = DailySummaryGenerator(token, USER_EMAIL)
engine.add_task(
    name="Resumen diario",
    func=summary.send_summary,
    schedule_config={"type": "daily", "time": "08:00"}
)

# Iniciar
if __name__ == "__main__":
    engine.start()