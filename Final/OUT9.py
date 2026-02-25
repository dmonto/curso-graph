"""
App Personal - Recordatorio Mensajes (Versión con Funciones)
    Login con Usuario Personal
    Leer Mensajes de ayer o anteriores sin abrir
    Incluir Inbox Personal, Inbox de cada Grupo Miembro, Mensajes de Teams
    Mostrar link para acceder a cada carpeta o mensaje
    Al concluir, debes: Subir el código aquí o al Sharepoint y comunicar en Teams con configuracion
"""

import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import json
from A0_1_get_delegated_token import get_delegated_token

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path, override=True)

# Configuración global
BASE_URL = "https://graph.microsoft.com/v1.0"


# ==================== FUNCIONES DE EMAIL ====================

def obtener_mesajes_sin_leer_personal(token, carpeta="inbox", dias_atras=1):
    """
    Obtener mensajes no leídos de ayer o anteriores.
    mailbox_type: 'inbox', 'drafts', 'sentitems', 'deleteditems'
    days_back: cuántos días hacia atrás buscar
    """
    emails = []
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Calcular fecha límite
        date_limit = (datetime.now() - timedelta(days=dias_atras)).date()
        
        # Construir filtro
        filter_query = f"isRead eq false and receivedDateTime le {date_limit}T23:59:59Z"
        
        # Obtener emails
        response = requests.get(
            f"{BASE_URL}/me/mailFolders/{carpeta}/messages",
            headers=headers,
            params={
                "$filter": filter_query,
                "$select": "id,subject,from,receivedDateTime,isRead,bodyPreview,webLink",
                "$orderby": "receivedDateTime desc",
                "$top": 50
            },
            timeout=30
        )
        
        if response.status_code == 200:
            messages = response.json().get("value", [])
            
            for msg in messages:
                emails.append({
                    "id": msg.get("id"),
                    "subject": msg.get("subject", "Sin asunto"),
                    "from": msg.get("from", {}).get("emailAddress", {}).get("name", "Desconocido"),
                    "from_email": msg.get("from", {}).get("emailAddress", {}).get("address", ""),
                    "received": msg.get("receivedDateTime"),
                    "preview": msg.get("bodyPreview", "")[:100],
                    "link": msg.get("webLink", ""),
                    "is_read": msg.get("isRead", False)
                })
            
            return emails
        else:
            print(f"❌ Error obteniendo emails: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def obtener_mensajes_sin_leer_grupo(token, group_id, group_name, carpeta="inbox", days_back=1):
    """Obtiene emails no leídos de un grupo específico."""
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Intentar obtener mensajes desde el mailbox del grupo
        url = f"{BASE_URL}/groups/{group_id}/mailFolders/{carpeta}/messages"
        resp = requests.get(
            url,
            headers=headers,
            params={
                "$filter": "isRead eq false",
                "$select": "id,subject,from,receivedDateTime,isRead,bodyPreview,webLink",
                "$orderby": "receivedDateTime desc",
                "$top": 50
            },
            timeout=30
        )

        emails = []

        if resp.status_code == 200:
            msgs = resp.json().get("value", [])
            for m in msgs:
                emails.append({
                    "id": m.get("id"),
                    "subject": m.get("subject", "Sin asunto"),
                    "from": m.get("from", {}).get("emailAddress", {}).get("name", "Desconocido"),
                    "from_email": m.get("from", {}).get("emailAddress", {}).get("address", ""),
                    "received": m.get("receivedDateTime"),
                    "preview": m.get("bodyPreview", "")[:100],
                    "link": m.get("webLink", ""),
                    "is_read": m.get("isRead", False)
                })

            return emails

        # Si no es accesible el mailbox, hacer fallback a conversations
        if resp.status_code >= 400:
            conv_resp = requests.get(
                f"{BASE_URL}/groups/{group_id}/conversations",
                headers=headers,
                params={"$top": 20},
                timeout=30
            )

            if conv_resp.status_code == 200:
                convs = conv_resp.json().get("value", [])
                for conv in convs:
                    emails.append({
                        "conversation_id": conv.get("id"),
                        "subject": conv.get("topic", "Sin asunto"),
                        "last_delivered": conv.get("lastDeliveredDateTime"),
                        "unique_senders": len(conv.get("uniqueSenders", [])),
                        "link": f"https://outlook.office.com/mail/group/{group_name}/conversations/{conv.get('id')}"
                    })

                return emails

            # si tampoco se puede, reportar el error del primer intento
            print(f"❌ Error accediendo mailbox del grupo {group_name}: {resp.status_code} - {resp.text}")
            return []

    except Exception as e:
        print(f"❌ Error en grupo {group_name}: {str(e)}")
        return []


def obtener_inbox_grupos(token, days_back=1):
    """Obtiene inboxes de todos los grupos de los que es miembro."""
    group_inboxes = []
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Obtener objetos de los que el usuario es miembro (memberOf).
        response = requests.get(
            f"{BASE_URL}/me/memberOf",
            headers=headers,
            params={
                "$select": "id,displayName,mail",
                "$top": 50
            },
            timeout=30
        )

        if response.status_code == 200:
            groups = response.json().get("value", [])

            for obj in groups:
                group_id = obj.get("id")
                group_name = obj.get("displayName")
                group_email = obj.get("mail")

                # Intentar obtener detalles del grupo vía /groups/{id}. Si no existe, se ignora.
                details = requests.get(
                    f"{BASE_URL}/groups/{group_id}",
                    headers=headers,
                    params={"$select": "mail,mailEnabled,displayName"},
                    timeout=10
                )
                if details.status_code != 200:
                    continue

                d = details.json()
                group_email = d.get("mail")
                mail_enabled = d.get("mailEnabled", False)
                if not group_email or not mail_enabled:
                    continue

                # Obtener emails no leídos del grupo (si tiene mailbox)
                emails = obtener_mensajes_sin_leer_grupo(token, group_id, group_name, carpeta="inbox", days_back=days_back)

                if emails:
                    group_inboxes.append({
                        "group_id": group_id,
                        "group_name": group_name,
                        "group_email": group_email,
                        "emails": emails
                    })

            return group_inboxes
        else:
            print(f"❌ Error obteniendo grupos: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"❌ Error al buscar inboxes de grupos: {str(e)}")
        return []


def get_chat_unread_count(token, chat_id, chat_data, days_back=1):
    """Obtiene información de no leídos en un chat (funcional)."""
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/me/chats/{chat_id}/messages",
            headers=headers,
            params={
                "$top": 5,
                "$orderby": "createdDateTime desc"
            },
            timeout=30
        )

        if response.status_code == 200:
            messages = response.json().get("value", [])

            unread_count = 0
            latest_message = None

            for msg in messages:
                # Determinar si es no leído (heurística: creado ayer o antes)
                created = msg.get("createdDateTime")
                if created:
                    msg_date = datetime.fromisoformat(created.replace('Z', '+00:00')).date()
                    yesterday = (datetime.now() - timedelta(days=days_back)).date()

                    if msg_date <= yesterday:
                        unread_count += 1
                        if not latest_message:
                            latest_message = msg

            return {
                "chat_id": chat_id,
                "topic": chat_data.get("topic", "Chat directo"),
                "chat_type": chat_data.get("chatType", ""),
                "unread_count": unread_count,
                "latest_message": latest_message.get("body", {}).get("content", "")[:100] if latest_message else "",
                "link": f"https://teams.microsoft.com/l/chat/{chat_id}/0"
            }
        else:
            return {"unread_count": 0}

    except Exception:
        return {"unread_count": 0}


def obtener_mensajes_teams_sin_leer_personal(token, days_back=1):
    """Obtiene mensajes no leídos de Teams (chats directos)."""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/me/chats",
            headers=headers,
            params={
                "$select": "id,topic,chatType,lastMessagePreview",
                "$top": 50
            },
            timeout=30
        )
        
        if response.status_code == 200:
            chats = response.json().get("value", [])
            
            unread_chats = []
            for chat in chats:
                # Obtener información de no leídos
                chat_info = get_chat_unread_count(token, chat.get("id"), chat)
                if chat_info.get("unread_count", 0) > 0:
                    unread_chats.append(chat_info)
            
            return unread_chats
        else:
            print(f"❌ Error obteniendo Teams: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def obtener_mensajes_teams_sin_leer_group(token, days_back=1):
    """Obtiene mensajes no leídos de canales de Teams."""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Obtener todos los teams del usuario
        response = requests.get(
            f"{BASE_URL}/me/joinedTeams",
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            return []
        
        teams = response.json().get("value", [])
        all_channel_messages = []
        
        for team in teams:
            team_id = team.get("id")
            team_name = team.get("displayName")
            
            # Obtener canales del team
            channels_response = requests.get(
                f"{BASE_URL}/teams/{team_id}/channels",
                headers=headers,
                timeout=30
            )
            
            if channels_response.status_code == 200:
                channels = channels_response.json().get("value", [])
                
                for channel in channels:
                    channel_id = channel.get("id")
                    channel_name = channel.get("displayName")
                    
                    # Obtener mensajes recientes
                    messages_response = requests.get(
                        f"{BASE_URL}/teams/{team_id}/channels/{channel_id}/messages",
                        headers=headers,
                        params={
                            "$top": 10
                        },
                        timeout=30
                    )
                    
                    if messages_response.status_code == 200:
                        messages = messages_response.json().get("value", [])
                        
                        # Filtrar mensajes antiguos
                        date_limit = datetime.now() - timedelta(days=days_back)
                        
                        for msg in messages:
                            msg_date = datetime.fromisoformat(
                                msg.get("createdDateTime", "").replace('Z', '+00:00')
                            )
                            try:    
                                if msg_date.date() <= date_limit.date():
                                    all_channel_messages.append({
                                        "team_name": team_name,
                                        "channel_name": channel_name,
                                        "from": msg.get("from", {}).get("user", {}).get("displayName", "Desconocido"),
                                        "subject": msg.get("subject", "Sin asunto"),
                                        "message": msg.get("body", {}).get("content", "")[:100],
                                        "created": msg.get("createdDateTime"),
                                        "link": msg.get("webUrl", "")
                                    })
                            except Exception:
                                continue
        
        return all_channel_messages
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


# ==================== FUNCIONES DE VISUALIZACIÓN Y REPORTES ====================

def mostrar_mensajes_sin_leer(personal_inbox, groups, teams_chats, channels):
    """Muestra todos los mensajes sin abrir de forma organizada."""
    
    print("\n" + "=" * 100)
    print("📬 MENSAJES SIN ABRIR - EMAIL Y TEAMS")
    print("=" * 100 + "\n")
    
    # 1. Inbox Personal
    if personal_inbox:
        print(f"📧 INBOX PERSONAL ({len(personal_inbox)} mensajes sin abrir)\n")
        for i, email in enumerate(personal_inbox, 1):
            print(f"  {i}. {email['subject']}")
            print(f"     📤 De: {email['from']} ({email['from_email']})")
            print(f"     📅 Recibido: {email['received']}")
            print(f"     📝 Previa: {email['preview']}")
            print(f"     🔗 Link: {email['link']}")
            print()
    
    # 2. Inboxes de Grupos
    if groups:
        print(f"\n👥 INBOXES DE GRUPOS ({len(groups)} grupos)\n")
        for group in groups:
            print(f"  📧 Grupo: {group['group_name']} ({group['group_email']})")
            print(f"     Mensajes sin abrir: {len(group['emails'])}")
            for email in group['emails'][:5]:  # Mostrar máximo 5
                print(f"       - {email['subject']}")
                print(f"         🔗 Link: {email.get('link', 'N/A')}")
            print()
    
    # 3. Chats de Teams
    if teams_chats:
        print(f"\n💬 TEAMS - CHATS DIRECTOS ({len(teams_chats)} chats sin abrir)\n")
        for i, chat in enumerate(teams_chats, 1):
            print(f"  {i}. {chat['topic']}")
            print(f"     💬 Tipo: {chat['chat_type']}")
            print(f"     📊 Mensajes sin abrir: {chat['unread_count']}")
            print(f"     📝 Último mensaje: {chat['latest_message']}")
            print(f"     🔗 Link: {chat['link']}")
            print()
    
    # 4. Canales de Teams
    if channels:
        print(f"\n📢 TEAMS - CANALES ({len(channels)} mensajes sin abrir)\n")
        for msg in channels[:20]:  # Mostrar máximo 20
            print(f"  Team: {msg['team_name']} | Canal: {msg['channel_name']}")
            print(f"     👤 De: {msg['from']}")
            print(f"     📝 Mensaje: {msg['message']}")
            print(f"     📅 Fecha: {msg['created']}")
            print(f"     🔗 Link: {msg['link']}")
            print()

    """Muestra todos los mensajes sin abrir de forma organizada."""
    
    print("\n" + "=" * 100)
    print("📬 MENSAJES SIN ABRIR - EMAIL Y TEAMS")
    print("=" * 100 + "\n")
    
    # 1. Inbox Personal
    if personal_inbox:
        print(f"📧 INBOX PERSONAL ({len(personal_inbox)} mensajes sin abrir)\n")
        for i, email in enumerate(personal_inbox, 1):
            print(f"  {i}. {email['subject']}")
            print(f"     📤 De: {email['from']} ({email['from_email']})")
            print(f"     📅 Recibido: {email['received']}")
            print(f"     📝 Previa: {email['preview']}")
            print(f"     🔗 Link: {email['link']}")
            print()
    
    # 2. Inboxes de Grupos
    if groups:
        print(f"\n👥 INBOXES DE GRUPOS ({len(groups)} grupos)\n")
        for group in groups:
            print(f"  📧 Grupo: {group['group_name']} ({group['group_email']})")
            print(f"     Mensajes sin abrir: {len(group['emails'])}")
            for email in group['emails'][:5]:  # Mostrar máximo 5
                print(f"       - {email['subject']}")
                print(f"         🔗 Link: {email.get('link', 'N/A')}")
            print()

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal del programa."""
    
    SCOPES = [
        "https://graph.microsoft.com/Mail.Read",
        "https://graph.microsoft.com/Team.ReadBasic.All",
        "https://graph.microsoft.com/ChannelMessage.Read.All",
        "https://graph.microsoft.com/Chat.ReadBasic"
    ]
    
    print("\n" + "=" * 100)
    print("🔐 LECTOR DE MENSAJES ANTIGUOS SIN ABRIR")
    print("=" * 100 + "\n")
    
    try:
        # 1. Obtener token
        print("1️⃣ - OBTENER TOKEN\n")
        token = get_delegated_token(SCOPES)
        
        # 2. Leer Emails
        print("2️⃣ - LEER MENSAJES DE EMAIL\n")
        
        print("  📧 - Inbox Personal...")
        personal_inbox = obtener_mesajes_sin_leer_personal(token, carpeta="inbox", dias_atras=0)
        print(f"     ✓ {len(personal_inbox)} mensajes sin abrir\n")
        
        print("  👥 - Inbox de Grupos...")
        group_inboxes = obtener_inbox_grupos(token, days_back=0)
        print(f"     ✓ {len(group_inboxes)} grupo(s)\n")
        
        # 3. Leer Teams
        print("3️⃣ - LEER MENSAJES DE TEAMS\n")
        
        print("  💬 - Chats Directos...")
        teams_chats = obtener_mensajes_teams_sin_leer_personal(token, days_back=1)
        print(f"     ✓ {len(teams_chats)} chat(s) sin abrir\n")
        
        print("  📢 - Mensajes de Canales...")
        channel_messages = obtener_mensajes_teams_sin_leer_group(token, days_back=1)
        print(f"     ✓ {len(channel_messages)} mensajes sin abrir\n")
        
        # 4. Mostrar Resultados
        mostrar_mensajes_sin_leer(personal_inbox, group_inboxes, teams_chats, channel_messages)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()
