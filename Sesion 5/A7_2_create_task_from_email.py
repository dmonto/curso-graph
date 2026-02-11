import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite, Tasks.ReadWrite"]
token = get_delegated_token(SCOPES)

def get_todo_list_id(access_token, list_name="EmailTasks"):
    """Obtiene o crea lista To Do."""
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    # GET listas
    response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
    if response.status_code == 200:
        lists = response.json().get("value", [])
        for lst in lists:
            if lst["displayName"] == list_name:
                return lst["id"]
    
    # Crea nueva
    create_payload = {"displayName": list_name, "is_shared": False}
    response = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists", 
                            headers=headers, json=create_payload)
    if response.status_code == 201:
        print(f"✓ Lista creada: {list_name}")
        return response.json()["id"]
    return None

def create_task_from_email(access_token, email, list_name="EmailTasks"):
    """Convierte correo en tarea To Do (migrado de Planner)."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Extraer info email (igual)
    subject = email["subject"][:100]  # To Do title max ~250, pero seguro
    body_preview = email["bodyPreview"][:1000]  # bodyContent más flexible
    from_address = email["from"]["emailAddress"]["address"]
    msg_id = email["id"]
    msg_web_url = f"https://outlook.office.com/mail/item/{msg_id}"
    
    # Descripción mejorada
    description = f"""📧 CONVERTIDO DE EMAIL

👤 De: {from_address}
📋 Asunto: {email['subject']}
🔗 [Abrir Email]({msg_web_url})

📝 Preview:
{body_preview}

---
Creado: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""

    # DueDate: 3 días por default
    due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT18:00:00.0000000Z")
    
    # Payload To Do
    payload = {
        "title": f"📧 {subject}",
        "bodyContent": description,
        "bodyContentType": "html",  # Soporta Markdown-ish
        "dueDateTime": {
            "dateTime": due_date,
            "timeZone": "Europe/Madrid"
        },
        "reminderDateTime": {
            "dateTime": (datetime.now() + timedelta(days=3, hours=-2)).strftime("%Y-%m-%dT16:00:00.0000000Z"),
            "timeZone": "Europe/Madrid"
        },
        "importance": "high",
        "status": "notStarted",
        "linkedResources": [{
            "webUrl": msg_web_url,
            "applicationName": "Outlook",
            "displayName": f"Email: {subject}"
        }]
    }
    
    # GET/Crea lista
    list_id = get_todo_list_id(access_token, list_name)
    if not list_id:
        print("✗ Error obteniendo lista To Do")
        return None
    
    # POST task
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        task_id = response.json().get("id")
        print(f"✓ To Do Task creada en '{list_name}': {task_id}")
        print(f"  📱 Ver en: https://to-do.microsoft.com/tasks/{list_id}/{task_id}")
        return response.json()
    else:
        print(f"✗ Error To Do: {response.status_code}")
        print(response.text)
        return None
