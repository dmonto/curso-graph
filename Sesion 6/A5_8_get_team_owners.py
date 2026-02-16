def get_team_owners(access_token, team_id):
    """Obtiene solo los propietarios del equipo."""
    
    members = get_team_members(access_token, team_id)
    owners = [m for m in members if "owner" in m["roles"]]
    
    return owners

def get_team_members_by_role(access_token, team_id, role):
    """Obtiene miembros con un rol específico."""
    
    members = get_team_members(access_token, team_id)
    filtered = [m for m in members if role in m["roles"]]
    
    return filtered

# USO
owners = get_team_owners(access_token, team_id)
print(f"Propietarios: {len(owners)}")

members = get_team_members_by_role(access_token, team_id, "member")
print(f"Miembros: {len(members)}")