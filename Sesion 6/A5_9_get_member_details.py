def get_member_details(access_token, team_id, member_id):
    """Obtiene detalles de un miembro específico."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/members/{member_id}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        member = response.json()
        return {
            "id": member["id"],
            "name": member.get("displayName"),
            "email": member.get("email"),
            "roles": member.get("roles", []),
            "visible_history_start": member.get("visibleHistoryStartDateTime")
        }
    
    return None

# USO
details = get_member_details(access_token, team_id, member_id)
print(f"Miembro: {details['name']}")
print(f"Roles: {details['roles']}")