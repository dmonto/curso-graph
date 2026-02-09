import time
import uuid
import requests

def call_graph_with_telemetry(method: str, url: str, headers: dict | None = None, **kwargs):
    headers = headers.copy() if headers else {}
    trace_id = headers.get("client-request-id") or str(uuid.uuid4())
    headers["client-request-id"] = trace_id

    start = time.perf_counter()
    resp = requests.request(method, url, headers=headers, timeout=15, **kwargs)
    elapsed = time.perf_counter() - start

    telemetry = {
        "trace_id": trace_id,
        "url": url,
        "method": method,
        "status_code": resp.status_code,
        "duration_ms": int(elapsed * 1000),
        "graph_request_id": resp.headers.get("request-id"),
        "graph_client_request_id": resp.headers.get("client-request-id"),
    }

    return resp, telemetry