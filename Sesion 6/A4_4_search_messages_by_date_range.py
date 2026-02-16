def search_messages_by_date_range(access_token, team_id, channel_id, start_date, end_date):
    """Busca mensajes dentro de un rango de fechas."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Formato ISO para fechas
    start_iso = start_date.isoformat() + "Z"
    end_iso = end_date.isoformat() + "Z"
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        params={
            "$filter": f"createdDateTime ge {start_iso} and createdDateTime le {end_iso}",
            "$orderby": "createdDateTime desc"
        },
        timeout=30
    )
    
    if response.status_code == 200:
        messages = response.json().get("value", [])
        return [
            {
                "id": msg["id"],
                "author": msg.get("from", {}).get("user", {}).get("displayName"),
                "content": msg.get("body", {}).get("content"),
                "timestamp": msg.get("createdDateTime")
            }
            for msg in messages
        ]
    
    return []

# USO
from datetime import datetime, timedelta

start = datetime(2026, 1, 1)
end = datetime(2026, 2, 31)

messages = search_messages_by_date_range(access_token, team_id, channel_id, start, end)
print(f"Mensajes en enero: {len(messages)}")