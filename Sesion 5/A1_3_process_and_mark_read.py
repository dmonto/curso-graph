import os
import logging
import requests
from A1_2_download_attachments import download_all_attachments_from_message
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mail.ReadWrite permite leer Y marcar como leído
SCOPES = ["Mail.ReadWrite"]

def mark_as_read(token: str, message_id: str):
    """Marcar un mensaje como leído."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    body = {"isRead": True}
    
    resp = requests.patch(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}",
        headers=headers,
        json=body,
        timeout=15,
    )
    
    if resp.ok:
        logger.info(f"✅ Mensaje {message_id[:20]}... marcado como leído")
        return True
    else:
        logger.error(f"❌ Error marcando leído: {resp.text}")
        return False

def process_inbox_workflow(token):
    """
    Workflow:
    1. Leer mensajes no leídos
    2. Para cada uno: descargar adjuntos si tiene
    3. Marcar como leído
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # Paso 1: Listar no leídos
    params = {
        "$filter": "isRead eq false and hasAttachments eq true",
        "$select": "id,subject,from",
        "$top": 5,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    messages = resp.json().get("value", [])
    logger.info(f"Procesando {len(messages)} mensajes no leídos con adjuntos")
    
    for msg in messages:
        msg_id = msg['id']
        subject = msg['subject']
        
        logger.info(f"\n▶ Procesando: {subject}")
        
        download_all_attachments_from_message(token, msg_id, subject)
        
        mark_as_read(token, msg_id)

if __name__ == "__main__":
    token = get_delegated_token(SCOPES)
    process_inbox_workflow(token)