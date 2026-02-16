import requests
import os
from A0_1_get_token import get_apponly_token

def search_messages_by_text(access_token, team_id, channel_id, keyword, top=100):
    """Busca mensajes que contengan una palabra clave."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtener mensajes del canal
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        params={"$top": top},
        timeout=30
    )
    
    if response.status_code != 200:
        return []
    
    messages = response.json().get("value", [])
    
    # Filtrar por palabra clave
    results = []
    for msg in messages:
        content = msg.get("body", {}).get("content", "").lower()
        if keyword.lower() in content:
            results.append({
                "id": msg["id"],
                "author": msg.get("from", {}).get("user", {}).get("displayName"),
                "content": msg.get("body", {}).get("content"),
                "timestamp": msg.get("createdDateTime"),
                "matches": content.count(keyword.lower())
            })
    
    return results

# USO
token = get_apponly_token()
team_id = os.getenv("TEAM_ID") or input("Id de Team:")
channel_id = os.getenv("CHANNEL_ID") or input("Id de Channel:")
results = search_messages_by_text(
    token,
    team_id,
    channel_id,
    "presupuesto",
    top=200
)

print(f"Encontrados {len(results)} mensajes:")
for result in results:
    print(f"- {result['author']}: {result['matches']} menciones")