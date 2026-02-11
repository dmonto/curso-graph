import logging
from pathlib import Path
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Mail.Read"]

def find_messages_with_attachments(token, limit: int = 5):
    """Encontrar mensajes con adjuntos."""
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "$filter": "hasAttachments eq true",
        "$select": "id,subject,from,hasAttachments",
        "$top": limit,
    }
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    return resp.json().get("value", [])

def list_attachments(token: str, message_id: str):
    """Listar adjuntos de un mensaje."""
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    
    return resp.json().get("value", [])

def download_attachment(token: str, message_id: str, attachment_id: str, filename: str = None):
    """Descargar un adjunto a disco."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener metadata del adjunto
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}",
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    attachment_info = resp.json()
    
    if not filename:
        filename = attachment_info['name']
    
    # Descargar contenido ($value devuelve bytes)
    resp_content = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}/$value",
        headers=headers,
        timeout=30,  # Archivos grandes pueden tardar
    )
    resp_content.raise_for_status()
    
    # Guardar a disco
    output_path = Path("downloads") / filename
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(resp_content.content)
    
    logger.info(f"✅ Descargado: {output_path} ({len(resp_content.content)} bytes)")
    
    return str(output_path)

def download_all_attachments_from_message(token: str, message_id: str, subject: str):
    """Descargar todos los adjuntos de un mensaje."""
    attachments = list_attachments(token, message_id)
    
    logger.info(f"Descargando {len(attachments)} adjuntos de: '{subject}'")
    
    downloaded = []
    for att in attachments:
        att_id = att['id']
        att_name = att['name']
        att_size = att.get('size', 0)
        
        logger.info(f"  Adjunto: {att_name} ({att_size} bytes)")
        
        path = download_attachment(token, message_id, att_id, att_name)
        downloaded.append(path)
    
    return downloaded

if __name__ == "__main__":
    token = get_delegated_token(SCOPES)
    
    # Paso 1: Encontrar mensajes con adjuntos
    logger.info("=== Buscando mensajes con adjuntos ===")
    messages = find_messages_with_attachments(token, limit=3)
    
    for msg in messages:
        logger.info(f"\nMensaje: {msg['subject']}")
        logger.info(f"De: {msg['from']['emailAddress']['name']}")
        
        # Paso 2: Descargar todos los adjuntos
        downloaded = download_all_attachments_from_message(token, msg['id'], msg['subject'])
        logger.info(f"Descargados {len(downloaded)} archivos")