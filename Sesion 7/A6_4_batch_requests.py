def batch_request(access_token, requests_list):
    """Ejecuta hasta 20 solicitudes en una llamada."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Construcción del payload
    batch_payload = {
        "requests": []
    }
    
    for i, req in enumerate(requests_list):
        batch_payload["requests"].append({
            "id": str(i),
            "method": req.get("method", "GET"),
            "url": req["url"]
        })
    
    response = requests.post(
        "https://graph.microsoft.com/v1.0/$batch",
        headers=headers,
        json=batch_payload,
        timeout=60
    )
    
    response.raise_for_status()
    
    results = response.json().get("responses", [])
    
    return results

# USO
requests_batch = [
    {"method": "GET", "url": "/drives/{id}/items/id1"},
    {"method": "GET", "url": "/drives/{id}/items/id2"},
    {"method": "GET", "url": "/drives/{id}/items/id3"},
    # ... hasta 20
]

results = batch_request(token, requests_batch)
for result in results:
    print(f"ID {result['id']}: {result.get('status')}")