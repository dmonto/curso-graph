def generate_membership_report(access_token, team_id):
    """Genera un reporte completo de miembros."""
    
    members = get_team_members(access_token, team_id)
    
    report = {
        "total_members": len(members),
        "owners": [],
        "members": [],
        "guests": []
    }
    
    for member in members:
        member_info = {
            "name": member["name"],
            "email": member["email"],
            "roles": member["roles"]
        }
        
        if "owner" in member["roles"]:
            report["owners"].append(member_info)
        else:
            report["members"].append(member_info)
    
    return report

# USO
report = generate_membership_report(access_token, team_id)
print(f"Miembros totales: {report['total_members']}")
print(f"Propietarios: {len(report['owners'])}")
print(f"Miembros: {len(report['members'])}")