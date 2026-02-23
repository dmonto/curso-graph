from apscheduler.schedulers.background import BackgroundScheduler # pip install apscheduler
from apscheduler.triggers.cron import CronTrigger
import logging

class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_jobs()
    
    def setup_jobs(self):
        """Configura todos los jobs."""
        
        # Job diario
        self.scheduler.add_job(
            self.daily_backup,
            CronTrigger(hour=2, minute=0),
            id='daily_backup',
            name='Daily Backup',
            misfire_grace_time=900
        )
        
        # Job cada 6 horas
        self.scheduler.add_job(
            self.sync_data,
            CronTrigger(hour='*/6'),
            id='sync_data',
            name='Sync Data',
            max_instances=1
        )
        
        # Job semanalmente
        self.scheduler.add_job(
            self.generate_report,
            CronTrigger(day_of_week='mon', hour=9, minute=0),
            id='weekly_report',
            name='Weekly Report'
        )
    
    def daily_backup(self):
        logging.info("Ejecutando backup diario...")
        # Tu lógica
    
    def sync_data(self):
        logging.info("Sincronizando datos...")
        # Tu lógica
    
    def generate_report(self):
        logging.info("Generando reporte semanal...")
        # Tu lógica
    
    def start(self):
        self.scheduler.start()
        logging.info("Scheduler iniciado")
    
    def stop(self):
        self.scheduler.shutdown()

# USO
scheduler = JobScheduler()
scheduler.start()
# scheduler.stop()