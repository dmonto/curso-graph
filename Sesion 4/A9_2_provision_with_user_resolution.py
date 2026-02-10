import os
import logging
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def resolve_user_by_email(email: str, token: str):
    """Resolver usuario por email para obtener ID."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"$filter": f"userPrincipalName eq '{email}'", "$select": "id"}
    
    resp = requests.get(
        "https://graph.microsoft.com/v1.0/users",
        headers=headers,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    
    users = resp.json().get("value", [])
    if not users:
        raise ValueError(f"Usuario no encontrado: {email}")
    
    return users[0]["id"]

def provision_from_csv(csv_data: list):
    """
    Provisionar desde datos CSV.
    csv_data: [
        {"team_name": "Project Alpha", "owner_email": "alice@contoso.com", ...},
        ...
    ]
    """
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    for team_config in csv_data:
        team_name = team_config['team_name']
        owner_email = team_config.get('owner_email')
        member_emails = team_config.get('member_emails', [])
        
        logger.info(f"Procesando: {team_name}")
        
        # Resolver emails a IDs
        try:
            members = []
            if owner_email:
                owner_id = resolve_user_by_email(owner_email, token)
                members.append({"id": owner_id, "role": "owner"})
            
            for member_email in member_emails:
                member_id = resolve_user_by_email(member_email, token)
                members.append({"id": member_id, "role": "member"})
            
            logger.info(f"  Resueltos {len(members)} usuarios")
            # Aquí llamarías a provision_full_workflow() con los miembros resueltos
        
        except ValueError as e:
            logger.error(f"  ❌ {e}")
            continue

if __name__ == "__main__":
    # Datos de entrada (podrían venir de CSV real)
    teams_data = [
        {
            "team_name": "Project Alpha",
            "owner_email": "alice@contoso.com",
            "member_emails": ["bob@contoso.com", "charlie@contoso.com"],
        },
        {
            "team_name": "Project Beta",
            "owner_email": "david@contoso.com",
            "member_emails": ["eve@contoso.com"],
        },
    ]
    
    provision_from_csv(teams_data)