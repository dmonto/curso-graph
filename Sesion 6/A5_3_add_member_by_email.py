def add_member_by_email(access_token, team_id, email, role="member"):
    """Agrega un miembro por email."""
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Primero obtener user_id del email
    user_response = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{email}",
        headers=headers,
        timeout=30
    )
    
    if user_response.status_code != 200:
        return {"status": "user_not_found", "email": email}
    
    user_id = user_response.json()["id"]
    
    # Agregar al equipo
    return add_member_to_team(access_token, team_id, user_id, role)

# USO
result = add_member_by_email(access_token, team_id, "usuario@example.com", role="member")