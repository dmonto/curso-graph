def mention_team(access_token, team_id, channel_id, team_mention_name, message_text):
    """Menciona a todo el equipo o un grupo."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Mención especial para equipos
    html_content = f'<at id="0">{team_mention_name}</at> {message_text}'
    
    payload = {
        "body": {
            "contentType": "html",
            "content": html_content
        },
        "mentions": [
            {
                "id": 0,
                "mentionText": team_mention_name,
                "mentioned": {
                    "conversation": {
                        "id": team_id,
                        "displayName": team_mention_name
                    }
                }
            }
        ]
    }
    
    response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    return response.status_code == 201