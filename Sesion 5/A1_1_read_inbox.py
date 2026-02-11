import logging
from datetime import datetime, timedelta, timezone
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Permisos delegados: Mail.Read para leer, Mail.ReadWrite para marcar leído
SCOPES = ["Mail.Read"]

def format_graph_datetime(dt: datetime) -> str:
    """Formato estricto para filtros Graph: YYYY-MM-DDTHH:MM:SSZ sin micros/offset."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def read_inbox_unread(token):
    """Leer mensajes no leídos de la bandeja de entrada."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Filtrar: no leídos, ordenar por fecha descendente
    params = {
        "$filter": "isRead eq false",
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments,bodyPreview",
        "$top": 10,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    messages = resp.json().get("value", [])
    logger.info(f"Encontrados {len(messages)} mensajes no leídos")
    
    for msg in messages:
        print(f"\n{'='*60}")
        print(f"De: {msg['from']['emailAddress']['name']} <{msg['from']['emailAddress']['address']}>")
        print(f"Asunto: {msg['subject']}")
        print(f"Recibido: {msg['receivedDateTime']}")
        print(f"Adjuntos: {'Sí' if msg['hasAttachments'] else 'No'}")
        print(f"Preview: {msg.get('bodyPreview', 'N/A')[:100]}")
    
    return messages

def read_recent_messages(token, days: int = 1, unread_only: bool = False):
    """Leer mensajes recientes (últimos N días)."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Fecha hace N días
    start_date = format_graph_datetime(datetime.now(timezone.utc) - timedelta(days=days))
    
    # Construir filtro
    filter_expr = f"receivedDateTime gt {start_date}"
    if unread_only:
        filter_expr += " and isRead eq false"
    
    params = {
        "$filter": filter_expr,
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments",
        "$top": 20,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    messages = resp.json().get("value", [])
    logger.info(f"Encontrados {len(messages)} mensajes en los últimos {days} días")
    
    return messages

if __name__ == "__main__":
    logger.info("=== Autenticando ===")
    token = get_delegated_token(SCOPES)

    logger.info("=== Leyendo bandeja de entrada ===")
    messages = read_inbox_unread(token)
    
    logger.info("\n=== Leyendo últimos 3 días (sin leer) ===")
    recent = read_recent_messages(token, days=3, unread_only=True)