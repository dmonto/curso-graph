import base64
import logging
import requests
from pathlib import Path
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Mail.Send"]

def create_draft(token: str, to_address: str, subject: str, body_text: str):
    """Crear borrador."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "subject": subject,
        "body": {
            "contentType": "text",
            "content": body_text,
        },
        "toRecipients": [
            {"emailAddress": {"address": to_address}}
        ],
    }
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/messages",
        headers=headers,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    
    message = resp.json()
    logger.info(f"✅ Borrador creado: {message['id']}")
    
    return message['id']

def add_attachment(token: str, message_id: str, file_path: str):
    """Agregar adjunto a un mensaje."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Leer archivo y encodear en base64
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    content_bytes = base64.b64encode(file_content).decode()
    filename = Path(file_path).name
    
    payload = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": filename,
        "contentBytes": content_bytes,
    }
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments",
        headers=headers,
        json=payload,
        timeout=30,  # Archivos grandes pueden tardar
    )
    resp.raise_for_status()
    
    logger.info(f"✅ Adjunto '{filename}' agregado")

def send_message(token: str, message_id: str):
    """Enviar un borrador."""
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/send",
        headers=headers,
        timeout=15,
    )
    
    if resp.status_code == 202:
        logger.info(f"✅ Correo enviado")
        return True
    else:
        logger.error(f"❌ Error: {resp.text}")
        return False

def send_email_with_attachments(to_address: str, subject: str, body_text: str, file_paths: list):
    """Workflow completo: crear draft, agregar adjuntos, enviar."""
    token = get_delegated_token(SCOPES)
    
    try:
        # Paso 1: Crear draft
        msg_id = create_draft(token, to_address, subject, body_text)
        
        # Paso 2: Agregar adjuntos
        for file_path in file_paths:
            if Path(file_path).exists():
                add_attachment(token, msg_id, file_path)
            else:
                logger.warning(f"⚠️ Archivo no encontrado: {file_path}")
        
        # Paso 3: Enviar
        send_message(token, msg_id)
        
        logger.info("✅ Flujo completo exitoso")
        return True
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    send_email_with_attachments(
        to_address="test@cursograph.onmicrosoft.com",
        subject="Documentos Importantes",
        body_text="Adjunto encontrarás los documentos solicitados.",
        file_paths=[
            "report.pdf",
            "data.xlsx",
        ],
    )