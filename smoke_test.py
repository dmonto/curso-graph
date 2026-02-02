import os
from dotenv import load_dotenv
import msal
import requests
import json

load_dotenv()

# === CONFIG DELEGATED ===
tenant_id = os.getenv("TENANT_ID")
client_id_delegated = os.getenv("CLIENT_ID_DELEGATED")
authority = f"https://login.microsoftonline.com/{tenant_id}"

scopes = [
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/User.Read.All",
    "https://graph.microsoft.com/Files.Read",
    "https://graph.microsoft.com/Group.Read.All",
    "https://graph.microsoft.com/GroupMember.Read.All",
    "https://graph.microsoft.com/Tasks.Read"
]

# === CONFIG APP-ONLY ===
client_id_apponly = os.getenv("CLIENT_ID_APPONLY")
client_secret = os.getenv("CLIENT_SECRET")
authority_apponly = authority  # mismo tenant


def check_delegated():
    print("🔐 [DELEGATED] Autenticando con PublicClientApplication...")
    app = msal.PublicClientApplication(client_id_delegated, authority=authority)
    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" not in result:
        print("❌ [DELEGATED] Error:", result.get("error"), result.get("error_description"))
        return False

    token = result["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    results = {}

    # 1. ME
    results['me'] = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
    print(f"✅ [DELEGATED] ME: {results['me']['displayName']} ({results['me']['userPrincipalName']})")

    # 2. USERS
    results['users'] = requests.get("https://graph.microsoft.com/v1.0/users?$top=1", headers=headers).json()
    print(f"✅ [DELEGATED] USERS: {len(results['users'].get('value', []))} usuarios visibles")

    # 3. GRAPH EXPLORER
    print("✅ [DELEGATED] GRAPH EXPLORER: Token válido → https://developer.microsoft.com/graph/graph-explorer")

    # 4. ONEDRIVE
    onedrive = requests.get("https://graph.microsoft.com/v1.0/me/drive", headers=headers).json()
    used_mb = onedrive.get('quota', {}).get('used', 0) / 1024**2
    print(f"✅ [DELEGATED] ONEDRIVE: {onedrive.get('name', 'Drive')} ({used_mb:.1f} MB usados)")

    # 5. TEAMS/GROUPS (busca grupo con 'Curso' o 'Graph')
    groups_url = "https://graph.microsoft.com/v1.0/me/memberOf?$select=id,displayName"
    groups = requests.get(groups_url, headers=headers).json()

    curso_groups = []
    for g in groups.get('value', []):
        name = g.get('displayName')
        if isinstance(name, str) and (name.startswith('Curso') or name.startswith('Graph')):
            curso_groups.append(g)

    for group in curso_groups:
        print(f"✅ [DELEGATED] GROUP: {group['displayName']} (id: {group['id'][:8]})")
        members = requests.get(
            f"https://graph.microsoft.com/v1.0/groups/{group['id']}/members?$top=5",
            headers=headers
        ).json()
        print(f"   👥 Miembros: {len(members.get('value', []))}")

    # 6. SHAREPOINT (drive del grupo)
    if curso_groups:
        group_id = curso_groups[0]['id']
        site_drive = requests.get(
            f"https://graph.microsoft.com/v1.0/groups/{group_id}/drive",
            headers=headers
        ).json()
        print(f"✅ [DELEGATED] SHAREPOINT: {site_drive.get('name')} ({site_drive.get('webUrl')})")

    # 7. PLANNER
    plans = requests.get("https://graph.microsoft.com/v1.0/me/planner/plans", headers=headers).json()
    print(f"✅ [DELEGATED] PLANNER: {len(plans.get('value', []))} planes")
    for plan in plans.get('value', [])[:3]:
        print(f"   📋 {plan.get('title')}")

    # Guardar resultados mínimos
    results['groups'] = curso_groups
    results['planner_plans'] = plans.get('value', [])

    with open('setup_completo_delegated.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("💾 [DELEGATED] setup_completo_delegated.json guardado")
    print("🎉 [DELEGATED] SETUP DELEGATED OK")
    return True


def check_app_only():
    print("\n🔐 [APP-ONLY] Autenticando con ConfidentialClientApplication...")
    app = msal.ConfidentialClientApplication(
        client_id=client_id_apponly,
        client_credential=client_secret,
        authority=authority_apponly,
    )

    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in result:
        print("❌ [APP-ONLY] Error:", result.get("error"), result.get("error_description"))
        return False

    token = result["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Ejemplo simple: listar 3 usuarios vía app-only
    users = requests.get("https://graph.microsoft.com/v1.0/users?$top=3", headers=headers).json()
    count = len(users.get('value', []))
    print(f"✅ [APP-ONLY] Token válido. Usuarios accesibles: {count}")

    with open('setup_completo_apponly.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    print("💾 [APP-ONLY] setup_completo_apponly.json guardado")
    print("🎉 [APP-ONLY] SETUP APP-ONLY OK")
    return True


if __name__ == "__main__":
    ok_delegated = check_delegated()
    ok_apponly = check_app_only()

    if ok_delegated and ok_apponly:
        print("\n🚀 TODO OK: ENTORNO LISTO PARA EL CURSO (DELEGATED + APP-ONLY)")
    elif ok_delegated:
        print("\n⚠️ SOLO DELEGATED OK: revisar credenciales de APP-ONLY")
    elif ok_apponly:
        print("\n⚠️ SOLO APP-ONLY OK: revisar configuración de APP DELEGATED")
    else:
        print("\n❌ NINGUNA APP OK: revisar .env y permisos en Entra ID")
