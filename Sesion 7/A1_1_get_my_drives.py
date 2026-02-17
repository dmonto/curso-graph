import requests
import os
from A0_1_get_token import get_delegated_token
from dotenv import load_dotenv

load_dotenv()

def list_my_teams_drives(token):
    """Todos drives que ves en Teams OneDrive."""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🏢 Tus Drives Teams/Grupos:")
    print("="*60)
    
    # 1. ME drives (incluye raíz + grupos)
    resp = requests.get("https://graph.microsoft.com/v1.0/me/drive", headers=headers)
    if resp.status_code == 200:
        me_drive = resp.json()
        print(f"👤 Personal: {me_drive['name']} ({me_drive['driveType']}/{me_drive['id']})")
        print(f"   {me_drive['webUrl']}")
    
    # 2. Joined Groups/Teams drives
    resp = requests.get("https://graph.microsoft.com/v1.0/me/joinedTeams?$select=id,displayName", headers=headers)
    teams = resp.json().get("value", [])
    for team in teams[:5]:  # Primeros 5
        resp = requests.get(f"https://graph.microsoft.com/v1.0/groups/{team['id']}/drive", headers=headers)
        if resp.status_code == 200:
            drive = resp.json()
            print(f"👥 {team['displayName'][:30]}...")
            print(f"   📁 {drive['name']} ({drive['driveType']}/{drive['id']})")
            print(f"   🔗 {drive['webUrl']}")
        print()
    
    # 3. Sites/Listas
    print("📋 Listas/Sites:")
    resp = requests.get("https://graph.microsoft.com/v1.0/sites?search=*&$top=3", headers=headers)
    for site in resp.json().get("value", []):
        resp = requests.get(f"https://graph.microsoft.com/v1.0/sites/{site['id']}/drives", headers=headers)
        drives = resp.json().get("value", [])
        for d in drives:
            print(f"   {site['displayName'][:20]} → {d['name']} ({d['id']})")


# USO
token = get_delegated_token(["Files.Read"])
list_my_teams_drives(token)
