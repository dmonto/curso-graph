import logging
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mail.Send permite enviar correos
SCOPES = ["Mail.Send"]

def send_simple_email(to_address: str, subject: str, body_text: str):
    """Enviar correo simple (texto)."""
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "text",
                "content": body_text,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_address,
                    }
                }
            ],
        },
        "saveToSentItems": True,
    }
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.status_code == 202:  # 202 Accepted (envío en background)
        logger.info(f"✅ Correo enviado a {to_address}")
        return True
    else:
        logger.error(f"❌ Error enviando correo: {resp.text}")
        return False

if __name__ == "__main__":
    send_simple_email(
        to_address="test@cursograph.onmicrosoft.com",
        subject="Reunión Mañana",
        body_text="Hablemos del curso.\n\nChao",
    )