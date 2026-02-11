import logging
import json
from datetime import datetime
from functools import wraps
import uuid
import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

# Configurar logger de auditoría
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

handler = logging.FileHandler("audit.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
audit_logger.addHandler(handler)

def audit_operation(operation_type="API_CALL"):
    """Decorator para auditar operaciones automáticamente."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar ID único para operación
            operation_id = str(uuid.uuid4())
            
            # Registrar inicio
            start_time = datetime.utcnow()
            
            audit_entry = {
                "operation_id": operation_id,
                "operation_type": operation_type,
                "function": func.__name__,
                "timestamp": start_time.isoformat(),
                "status": "started"
            }
            
            try:
                # Ejecutar función
                result = func(*args, **kwargs)
                
                # Registrar éxito
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000
                
                audit_entry.update({
                    "status": "success",
                    "duration_ms": duration_ms,
                    "timestamp_end": end_time.isoformat(),
                    "result_summary": str(result)[:100]  # Primeros 100 chars
                })
                
                audit_logger.info(json.dumps(audit_entry))
                return result
            
            except Exception as e:
                # Registrar error
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000
                
                audit_entry.update({
                    "status": "failed",
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_ms": duration_ms,
                    "timestamp_end": end_time.isoformat()
                })
                
                audit_logger.warning(json.dumps(audit_entry))
                raise
        
        return wrapper
    return decorator

# Uso
@audit_operation("GET_EMAILS")
def get_user_emails(access_token, top=10):
    """Obtiene correos del usuario."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages?$top={top}",
        headers=headers
    )
    return response.json()