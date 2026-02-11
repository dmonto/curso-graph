import logging
import re
import requests
from A0_1_get_token import get_delegated_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["Mail.Send"]

def validate_email(email: str) -> bool:
    """Validar formato de email básico."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def sanitize_html(html_content: str) -> str:
    """Sanitizar HTML básico (remover scripts peligrosos)."""
    # Esta es una sanitización muy simple; para producción usar bleach library
    import re
    
    # Remover <script> tags
    html_content = re.sub(r"<script.*?</script>", "", html_content, flags=re.DOTALL)
    # Remover event handlers (onclick, onerror, etc.)
    html_content = re.sub(r'\s+on\w+\s*=\s*["\'].*?["\']', "", html_content)
    
    return html_content

def send_html_email(
    to_addresses: list,
    cc_addresses: list,
    subject: str,
    html_body: str,
    importance: str = "normal",
):
    """Enviar correo HTML con validación."""
    
    # Validar direcciones
    for email in to_addresses + cc_addresses:
        if not validate_email(email):
            logger.error(f"❌ Email inválido: {email}")
            return False
    
    # Sanitizar HTML
    html_body = sanitize_html(html_body)
    
    token = get_delegated_token(SCOPES)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construir recipients
    to_recipients = [
        {"emailAddress": {"address": addr}} for addr in to_addresses
    ]
    cc_recipients = [
        {"emailAddress": {"address": addr}} for addr in cc_addresses
    ] if cc_addresses else []
    
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "html",
                "content": html_body,
            },
            "toRecipients": to_recipients,
            "ccRecipients": cc_recipients,
            "importance": importance,  # normal, high, low
            "categories": ["sent-via-api"],
        },
        "saveToSentItems": True,
    }
    
    logger.info(f"Enviando correo HTML a {len(to_addresses)} destinatarios...")
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json=payload,
        timeout=15,
    )
    
    if resp.status_code == 202:
        logger.info(f"✅ Correo HTML enviado")
        return True
    else:
        logger.error(f"❌ Error: {resp.text}")
        return False

if __name__ == "__main__":
    html_content = """
    <html>
    <body>
        <h2>Reporte Trimestral</h2>
        <p>Estimado usuario,</p>
        <p>Adjunto encontrarás el <b>reporte de Q1</b> con los siguientes puntos:</p>
        <ul>
            <li>Ventas: +15%</li>
            <li>Nuevos clientes: 42</li>
            <li>Retención: 98%</li>
        </ul>
        <p>Cualquier pregunta, contáctame.</p>
        <p>Saludos,<br/>El equipo</p>
    </body>
    </html>
    """
    
    send_html_email(
        to_addresses=["test@cursograph.onmicrosoft.com", "diego.montoliu@cursograph.onmicrosoft.com"],
        cc_addresses=["jefe@cursograph.onmicrosoft.com"],
        subject="Reporte Q1 - Datos Clave",
        html_body=html_content,
        importance="high",
    )