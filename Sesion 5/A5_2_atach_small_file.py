import base64
import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

def attach_small_file(access_token, message_id, file_path):
    """
    Adjunta un archivo pequeño (< 3 MB) directamente.
    Método simple y rápido.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Leer archivo
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    # Convertir a base64
    content_base64 = base64.b64encode(file_content).decode()
    
    # Preparar payload
    attachment = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": "documento.pdf",
        "contentBytes": content_base64
    }
    
    # Enviar
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"
    response = requests.post(url, headers=headers, json=attachment)
    
    if response.status_code == 201:
        attachment_id = response.json().get("id")
        print(f"Archivo adjuntado: {attachment_id}")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False

# Uso
attach_small_file(token, "message-id-here", "documento.pdf")