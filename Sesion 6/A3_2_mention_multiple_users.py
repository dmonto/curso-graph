def mention_multiple_users(access_token, team_id, channel_id, users_list, message_text):
    """Menciona a múltiples usuarios."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Construir HTML con múltiples menciones
    mentions_html = ""
    mentions_list = []
    
    for idx, user in enumerate(users_list):
        mentions_html += f'<at id="{idx}">{user["displayName"]}</at> '
        mentions_list.append({
            "id": idx,
            "mentionText": user["displayName"],
            "mentioned": {
                "user": {
                    "id": user["id"],
                    "displayName": user["displayName"]
                }
            }
        })
    
    html_content = mentions_html + message_text
    
    payload = {
        "body": {
            "contentType": "html",
            "content": html_content
        },
        "mentions": mentions_list
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    return response.status_code == 201

# USO
users = [
    {"id": "user1", "displayName": "Juan"},
    {"id": "user2", "displayName": "María"},
    {"id": "user3", "displayName": "Pedro"}
]

mention_multiple_users(
    access_token,
    team_id,
    channel_id,
    users,
    "revisar el reporte de ventas"
)