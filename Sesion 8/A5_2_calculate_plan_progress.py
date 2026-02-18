import requests
import os
from dotenv import load_dotenv
from A0_1_get_token import get_apponly_token
from A5_1_get_all_tasks import get_all_tasks

load_dotenv()

def calculate_plan_progress(tasks):
    """Calcula el progreso general del plan."""
    
    if not tasks:
        return 0
    
    total_progress = sum(t.get("percentComplete", 0) for t in tasks)
    avg_progress = total_progress / len(tasks)
    
    return round(avg_progress, 1)

def get_overdue_tasks(tasks):
    """Obtiene tareas vencidas."""
    
    from datetime import datetime, timezone
    
    now = datetime.now(timezone.utc)
    overdue = []
    
    for task in tasks:
        due_date = task.get("dueDateTime")
        if due_date:
            due_dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            
            if due_dt < now and task.get("percentComplete", 0) < 100:
                overdue.append(task)
    
    return overdue

def calculate_workload_by_user(tasks):
    """Calcula carga de trabajo por usuario."""
    
    workload = {}
    
    for task in tasks:
        assignments = task.get("assignments", {})
        
        for email in assignments.keys():
            if email not in workload:
                workload[email] = {
                    "total": 0,
                    "completed": 0,
                    "in_progress": 0,
                    "pending": 0,
                    "overdue": 0
                }
            
            workload[email]["total"] += 1
            
            percent = task.get("percentComplete", 0)
            if percent == 100:
                workload[email]["completed"] += 1
            elif percent > 0:
                workload[email]["in_progress"] += 1
            else:
                workload[email]["pending"] += 1
    
    return workload

def calculate_user_productivity(tasks):
    """Calcula productividad por usuario."""
    
    productivity = {}
    
    for task in tasks:
        assignments = task.get("assignments", {})
        
        for email in assignments.keys():
            if email not in productivity:
                productivity[email] = {
                    "tasks": [],
                    "avg_progress": 0,
                    "completion_rate": 0
                }
            
            productivity[email]["tasks"].append(task)
    
    # Calcular métricas
    for email, data in productivity.items():
        if data["tasks"]:
            total_progress = sum(t.get("percentComplete", 0) for t in data["tasks"])
            avg_progress = total_progress / len(data["tasks"])
            
            completed = sum(1 for t in data["tasks"] if t.get("percentComplete") == 100)
            completion_rate = (completed / len(data["tasks"])) * 100
            
            data["avg_progress"] = round(avg_progress, 1)
            data["completion_rate"] = round(completion_rate, 1)
    
    return productivity

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
tasks = get_all_tasks(token, plan_id)
progress = calculate_plan_progress(tasks)
print(f"Progreso plan: {progress}%")
print(get_overdue_tasks(tasks))
print(calculate_workload_by_user(tasks))
print(calculate_user_productivity(tasks))