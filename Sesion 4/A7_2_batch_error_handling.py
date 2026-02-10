import os
import logging
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_app_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def execute_batch_with_error_handling(batch_requests: list):
    """Ejecutar batch y manejar resultados parciales."""
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construir payload batch (máximo 20 requests, típicamente 15 por throttling)
    batch_payload = {
        "requests": batch_requests
    }
    
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/$batch",
        headers=headers,
        json=batch_payload,
        timeout=30,  # batch puede tardar más
    )
    
    if resp.status_code != 200:
        logger.error(f"Batch request falló con {resp.status_code}")
        error = resp.json().get("error", {})
        logger.error(f"Error: {error.get('message')}")
        return None
    
    # Procesar respuestas individuales
    batch_response = resp.json()
    responses = batch_response.get("responses", [])
    
    successes = []
    failures = []
    retryable = []
    
    for sub_resp in responses:
        request_id = sub_resp.get("id")
        status = sub_resp.get("status")
        body = sub_resp.get("body", {})
        
        if status == 200:
            successes.append({"id": request_id, "data": body})
            logger.info(f"✅ Request {request_id}: éxito")
        elif status == 404:
            failures.append({"id": request_id, "reason": "Not found"})
            logger.warning(f"⚠️ Request {request_id}: 404 Not Found")
        elif status == 429:
            # Throttling: puede reintentarse
            retryable.append({"id": request_id, "reason": "Too Many Requests"})
            logger.warning(f"⏳ Request {request_id}: 429 Throttled, puede reintentarse")
        elif status >= 400:
            error = body.get("error", {})
            failures.append({"id": request_id, "reason": error.get("message", "Unknown error")})
            logger.error(f"❌ Request {request_id}: {error.get('code')} - {error.get('message')}")
        else:
            logger.info(f"ℹ️ Request {request_id}: status {status}")
    
    logger.info(f"\nResumen batch:")
    logger.info(f"  Exitosos: {len(successes)}")
    logger.info(f"  Fallos no reintentables: {len(failures)}")
    logger.info(f"  Reintentables (429): {len(retryable)}")
    
    return {
        "successes": successes,
        "failures": failures,
        "retryable": retryable,
    }

if __name__ == "__main__":
    # Ejemplo: 3 requests en batch
    batch_reqs = [
        {
            "id": "1",
            "method": "GET",
            "url": "/users/invalid-id",
        },
        {
            "id": "2",
            "method": "GET",
            "url": "/users?$top=1&$select=id,displayName",
        },
        {
            "id": "3",
            "method": "PATCH",
            "url": "/users/another-invalid-id",
            "body": {"displayName": "New Name"},
        },
    ]
    
    result = execute_batch_with_error_handling(batch_reqs)
    if result:
        print("\nResultado completo:")
        print(f"  OK: {result['successes']}")
        print(f"  Fail: {result['failures']}")
        print(f"  Retry: {result['retryable']}")