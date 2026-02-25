import os
import requests
from datetime import datetime, timedelta, timezone
from msal import ConfidentialClientApplication, PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

# Configuración
CLIENT_ID_APPONLY = os.getenv("CLIENT_ID_APPONLY")
CLIENT_ID_DELEGATED = os.getenv("CLIENT_ID_DELEGATED")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PLAN_ID = os.getenv("PLAN_ID")  # ID del plan de Planner
GROUP_ID = os.getenv("GROUP_ID")  # ID del grupo
DIAS_VENCIMIENTO = int(os.getenv("DIAS_VENCIMIENTO", 7))  # Días para considerar vencimiento próximo

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES_APPONLY = ["https://graph.microsoft.com/.default"]
SCOPES_DELEGATED = ["Mail.Send", "ChannelMessage.Send"]

def get_app_token():
    """Obtiene token app-only para lectura de tareas."""
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID_APPONLY,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES_APPONLY)
    if "access_token" not in result:
        raise RuntimeError(f"Error MSAL (app-only): {result.get('error_description')}")
    return result["access_token"]

def get_delegated_token():
    """Obtiene token delegado para envío de correo y Teams."""
    app = PublicClientApplication(
        client_id=CLIENT_ID_DELEGATED,
        authority=AUTHORITY,
    )
    
    # Usar autenticación interactiva (device code flow)
    result = app.acquire_token_interactive(scopes=SCOPES_DELEGATED)
    
    if "access_token" not in result:
        raise RuntimeError(f"Error MSAL (delegado): {result.get('error_description')}")
    
    return result["access_token"]

def get_upcoming_tasks(token, plan_id, days_ahead):
    """Obtiene tareas que vencen en los próximos días."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Calcular fecha límite
    limit_date = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).strftime('%Y-%m-%dT23:59:59Z')
    
    params = {
        "$filter": f"dueDateTime le {limit_date}",
        "$select": "id,title,dueDateTime,percentComplete,assignments",
        "$orderby": "dueDateTime asc"
    }
    
    url = f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/tasks"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    tasks = response.json().get("value", [])
    # Filtrar tareas no completadas, que tengan fecha de vencimiento y que venzan en los próximos días
    upcoming_tasks = [
        task for task in tasks 
        if task.get("dueDateTime") and 
           task.get("percentComplete", 0) < 100 and 
           datetime.fromisoformat(task["dueDateTime"].replace('Z', '+00:00')) <= datetime.now(timezone.utc) + timedelta(days=days_ahead)
    ]

    #devuelve solo las tareas próximas a vencer
    return upcoming_tasks

    

def generate_summary_message(tasks):
    """Genera mensaje HTML simple con tabla de tareas."""
    if not tasks:
        return "<p><strong>No hay tareas próximas a vencer.</strong></p>"
    
    html = """
    <h3> Tareas Próximas</h3>
    <table style="border-collapse: collapse; width: 100%; font-family: Arial;">
        <tr style="background-color: #2E75B6; color: white;">
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Tarea</th>
            <th style="padding: 10px; text-align: center; border: 1px solid #ddd;">Vencimiento</th>
        </tr>
    """
    
    for task in tasks:
        title = task.get("title", "Sin título")
        due_date_str = task.get("dueDateTime", "Sin fecha")
        
        # Formatear fecha
        try:
            due_date_obj = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            due_date_formatted = due_date_obj.strftime('%d/%m/%Y')
        except:
            due_date_formatted = due_date_str
        
        html += f"""
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">{title}</td>
            <td style="padding: 10px; text-align: center; border: 1px solid #ddd;">{due_date_formatted}</td>
        </tr>
        """
    
    html += """
    </table>
    """
    
    return html

def get_group_email(token, group_id):
    """Obtiene el e-mail del grupo."""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}"
    params = {"$select": "mail"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("mail")

def send_group_email(token, group_id, subject, body):
    """Envía e-mail al grupo."""
    group_email = get_group_email(token, group_id)
    if not group_email:
        print(" No se pudo obtener el e-mail del grupo")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": group_email
                    }
                }
            ]
        }
    }
    
    url = f"https://graph.microsoft.com/v1.0/me/sendMail"
    response = requests.post(url, headers=headers, json=email_data)
    response.raise_for_status()
    print(" E-mail enviado al grupo")

def get_team_id_from_group(token, group_id):
    """Obtiene el team ID del grupo."""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/team"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def get_general_channel_id(token, team_id):
    """Obtiene el ID del canal general."""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    channels = response.json().get("value", [])
    for channel in channels:
        if channel.get("displayName") == "General":
            return channel.get("id")
    return None

def send_channel_message(token, team_id, channel_id, message):
    """Envía mensaje al canal."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    message_data = {
        "body": {
            "contentType": "html",
            "content": message
        }
    }
    
    url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
    response = requests.post(url, headers=headers, json=message_data)
    response.raise_for_status()
    print(" Mensaje enviado al canal general")

def main():
    try:
        # Obtener token app-only para lectura de tareas
        token_apponly = get_app_token()
        print("Token app-only obtenido correctamente")
        
        # Obtener tareas próximas
        tasks = get_upcoming_tasks(token_apponly, PLAN_ID, DIAS_VENCIMIENTO)
        print(f"Encontradas {len(tasks)} tareas próximas")
        
        # Generar mensaje
        summary = generate_summary_message(tasks)
        print("Mensaje resumen generado")
        
        # Obtener token delegado para envíos
        print("\nObteniendo token delegado para envíos...")
        token_delegated = get_delegated_token()
        print("Token delegado obtenido correctamente")
        
        # Enviar e-mail al grupo (usando token delegado)
        try:
            subject = f"Recordatorio: {len(tasks)} tareas próximas a vencer"
            send_group_email(token_delegated, GROUP_ID, subject, summary)
        except Exception as e:
            print(f"No se pudo enviar e-mail al grupo: {e}")
        
        # Enviar mensaje al canal general (usando token delegado)
        try:
            team_id = get_team_id_from_group(token_apponly, GROUP_ID)  # Obtenemos team_id con app-only
            if team_id:
                channel_id = get_general_channel_id(token_apponly, team_id)  # Obtenemos channel_id con app-only
                if channel_id:
                    send_channel_message(token_delegated, team_id, channel_id, summary)  # Enviamos con delegado
                else:
                    print(" No se encontró el canal General")
            else:
                print(" El grupo no tiene un equipo asociado")
        except Exception as e:
            print(f" No se pudo enviar mensaje al canal: {e}")
        
        print(" Proceso completado exitosamente")
        
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()
