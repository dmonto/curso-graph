from A0_1_get_token import get_delegated_token
from A7_1_get_emails_to_convert import get_emails_to_convert
from A7_2_create_task_from_email import create_task_from_email
import requests

SCOPES = ["Mail.ReadWrite, Tasks.ReadWrite"]
token = get_delegated_token(SCOPES)

def process_emails_to_tasks(access_token, plan_id, bucket_id, assigned_user_id, keywords=None):
    """Procesa correos y crea tareas automáticamente."""
    
    # Obtener correos válidos
    emails = get_emails_to_convert(access_token, keywords=keywords)
    
    created_tasks = []
    
    for email in emails:
        try:
            # Validaciones
            if not email["subject"] or len(email["subject"]) < 3:
                print(f"⊘ Asunto muy corto: {email['subject']}")
                continue
            
            # Crear tarea
            task = create_task_from_email(
                access_token,
                email,
                plan_id,
                bucket_id,
                assigned_user_id
            )
            
            if task:
                created_tasks.append({
                    "email_subject": email["subject"],
                    "task_id": task.get("id"),
                    "status": "created"
                })
                
                # Marcar correo como leído (opcional)
                mark_email_as_read(access_token, email["id"])
        
        except Exception as e:
            print(f"✗ Error procesando correo: {e}")
            continue
    
    print(f"\n✓ Total de tareas creadas: {len(created_tasks)}")
    return created_tasks

def mark_email_as_read(access_token, message_id):
    """Marca un correo como leído."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {"isRead": True}
    
    requests.patch(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}",
        headers=headers,
        json=payload
    )