import os
import time
import logging
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("CLIENT_ID_APPONLY")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_app_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

class TeamProvisioner:
    def __init__(self):
        self.token = get_app_token()
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    
    def create_team_group(self, display_name: str, description: str):
        """Crear un Grupo de Microsoft 365 (Teams)."""
        logger.info(f"Creando Team: {display_name}")
        
        body = {
            "displayName": display_name,
            "description": description,
            "groupTypes": ["Unified"],  # Unified = Microsoft 365 Group = Team[web:642]
            "mailEnabled": True,
            "securityEnabled": True,
            "mailNickname": display_name.replace(" ", "").lower(),
        }
        
        resp = requests.post(
            "https://graph.microsoft.com/v1.0/groups",
            headers=self.headers,
            json=body,
            timeout=15,
        )
        resp.raise_for_status()
        group = resp.json()
        logger.info(f"✅ Team creado: {group['id']}")
        return group['id']
    
    def add_members(self, team_id: str, member_list: list):
        """Agregar miembros (y owners) en bulk al Team."""
        logger.info(f"Agregando {len(member_list)} miembros al Team...")
        
        values = []
        for member in member_list:
            user_id = member['id']
            role = member.get('role', 'member')  # 'owner' o 'member'
            
            values.append({
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": [role],
                "user@odata.navigationSource": "directoryObjects",
                "user": {"id": user_id},
            })
        
        body = {"values": values}
        
        resp = requests.post(
            f"https://graph.microsoft.com/v1.0/teams/{team_id}/members/add",
            headers=self.headers,
            json=body,
            timeout=30,
        )
        resp.raise_for_status()
        logger.info(f"✅ Miembros agregados")
    
    def create_planner_plan(self, team_id: str, plan_title: str):
        """Crear Plan de Planner vinculado al Team."""
        logger.info(f"Creando Plan: {plan_title}")
        
        body = {
            "title": plan_title,
            "owner": team_id,  # Vincular al Team/Group[web:650]
        }
        
        resp = requests.post(
            "https://graph.microsoft.com/v1.0/planner/plans",
            headers=self.headers,
            json=body,
            timeout=15,
        )
        resp.raise_for_status()
        plan = resp.json()
        logger.info(f"✅ Plan creado: {plan['id']}")
        return plan['id']
    
    def create_buckets(self, plan_id: str, bucket_names: list):
        """Crear buckets (categorías) en el Plan."""
        logger.info(f"Creando {len(bucket_names)} buckets...")
        
        buckets = {}
        for name in bucket_names:
            body = {"name": name, "planId": plan_id}
            resp = requests.post(
                "https://graph.microsoft.com/v1.0/planner/buckets",
                headers=self.headers,
                json=body,
                timeout=15,
            )
            resp.raise_for_status()
            bucket = resp.json()
            buckets[name] = bucket['id']
            logger.info(f"  ✓ Bucket '{name}' creado")
        
        return buckets
    
    def create_task(self, plan_id: str, bucket_id: str, title: str, assigned_to: str):
        """Crear tarea asignada a un usuario."""
        logger.info(f"Creando tarea: {title} → {assigned_to}")
        
        body = {
            "planId": plan_id,
            "bucketId": bucket_id,
            "title": title,
            "assignments": {
                assigned_to: {
                    "@odata.type": "#microsoft.graph.plannerAssignment",
                    "orderHint": " !",
                }
            },
        }
        
        resp = requests.post(
            "https://graph.microsoft.com/v1.0/planner/tasks",
            headers=self.headers,
            json=body,
            timeout=15,
        )
        resp.raise_for_status()
        task = resp.json()
        logger.info(f"✅ Tarea creada: {task['id']}")
        return task['id']
    
    def provision_full_workflow(self, team_name: str, members: list, tasks: list):
        """
        Workflow completo:
        1. Crear Team
        2. Agregar miembros
        3. Crear Plan
        4. Crear buckets
        5. Crear tareas y asignar
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"INICIANDO PROVISIÓN: {team_name}")
        logger.info(f"{'='*60}\n")
        
        try:
            # Paso 1: Crear Team
            team_id = self.create_team_group(
                display_name=team_name,
                description=f"Team de {team_name} - provisión automática",
            )
            time.sleep(2)  # Pequeña pausa para que el backend se estabilice[web:642]
            
            # Paso 2: Agregar miembros
            self.add_members(team_id, members)
            
            # Paso 3: Crear Plan
            plan_title = f"{team_name} - Plan de tareas"
            plan_id = self.create_planner_plan(team_id, plan_title)
            
            # Paso 4: Crear buckets
            bucket_names = ["A hacer", "En progreso", "Completado"]
            buckets = self.create_buckets(plan_id, bucket_names)
            
            # Paso 5: Crear tareas
            for task_info in tasks:
                title = task_info['title']
                assigned_user = task_info['assigned_to']
                bucket_name = task_info.get('bucket', 'A hacer')
                bucket_id = buckets.get(bucket_name, list(buckets.values())[0])
                
                self.create_task(plan_id, bucket_id, title, assigned_user)
            
            logger.info(f"\n✅ PROVISIÓN COMPLETADA")
            logger.info(f"  Team ID: {team_id}")
            logger.info(f"  Plan ID: {plan_id}")
            
            return {"team_id": team_id, "plan_id": plan_id, "buckets": buckets}
        
        except Exception as e:
            logger.error(f"❌ Error durante provisión: {e}")
            raise

if __name__ == "__main__":
    provisioner = TeamProvisioner()
    
    # Definir miembros (necesitas IDs reales de usuarios)
    members = [
        {"id": "user-id-1", "role": "owner"},     # Project Lead
        {"id": "user-id-2", "role": "member"},    # Developer
        {"id": "user-id-3", "role": "member"},    # Designer
    ]
    
    # Definir tareas iniciales
    tasks = [
        {"title": "Configurar repositorio", "assigned_to": "user-id-2", "bucket": "A hacer"},
        {"title": "Diseñar mockups", "assigned_to": "user-id-3", "bucket": "A hacer"},
        {"title": "Revisar especificaciones", "assigned_to": "user-id-1", "bucket": "En progreso"},
    ]
    
    result = provisioner.provision_full_workflow(
        team_name="Project Alpha",
        members=members,
        tasks=tasks,
    )
    
    print(f"\nResultado: {result}")