#!/usr/bin/env python3
"""Proceso automático de tareas completadas en Planner.

1. Lee todas las tareas no completadas de un plan.
2. Obtiene el checklist de cada tarea.
3. Si al menos un elemento está marcado y no todos:
   * actualiza la tarea a "inProgress" (en curso) y ajusta percentComplete.
4. Si todos los elementos del checklist están marcados:
   * marca la tarea como "completed" y, opcionalmente, la mueve a un bucket
     de finalizadas (el id se pasa como parámetro o variable de entorno).

El script se ejecuta con permisos app-only (CLIENT_ID_APPONLY).
"""

""" Variables usadas para las pruebas:
************************************************************
TENANT_ID=a7b746ea-0f9f-454e-a288-d8c858c0a9c1
USER_ID=69706795-ec7f-4293-a3cd-31bf7202f9de
# === APP-ONLY ===
CLIENT_ID_APPONLY=ff17ceec-9605-4f82-b0f1-5318ce575e1b
BUCKET_COMPLETADAS=fX4pG8cYaUaVE5CqFCFPqZgADY0b
************************************************************
"""

import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from A0_1_get_token import get_apponly_token

# Cargar variables de entorno
load_dotenv()

# Listado para cada bucket de un plan, de las tareas no completadas (percentComplete < 100)
def list_open_tasks(access_token: str, plan_id: str) -> list:
    """Devuelve lista de tareas abiertas (percentComplete < 100) de un plan."""
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets", headers=headers)
    resp.raise_for_status()
    buckets = resp.json().get("value", [])
    open_tasks = []
    for b in buckets:
        bid = b.get("id")
        r2 = requests.get(f"https://graph.microsoft.com/v1.0/planner/buckets/{bid}/tasks", headers=headers)
        if r2.status_code != 200:
            continue
        for t in r2.json().get("value", []):
            if t.get("percentComplete", 0) < 100 and t.get("status") != "completed":
                open_tasks.append({
                    "id": t.get("id"),
                    "title": t.get("title"),
                    "percentComplete": t.get("percentComplete"),
                    "status": t.get("status"),
                    "bucketId": bid,
                })
    return open_tasks

# Obtenemos el checklist de una tarea (si existe) y lo devolvemos como diccionario.
def get_task_checklist(access_token: str, task_id: str) -> dict:
    """Recupera el diccionario de checklist (vacio si no existe)."""
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details", headers=headers)
    r.raise_for_status()
    return r.json().get("checklist", {})



def patch_task(access_token: str, task_id: str, patch_body: dict) -> dict | None:
    """Aplica un parche sobre la tarea con el ETag adecuado."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # obtener etag
    r = requests.get(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}", headers=headers)
    r.raise_for_status()
    etag = r.headers.get("ETag", "")
    headers["If-Match"] = etag
    r2 = requests.patch(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}", headers=headers, json=patch_body)
    if r2.status_code not in (200, 204):
        raise Exception(f"Error al parchear tarea {task_id}: {r2.text}")
    return r2.json() if r2.text else None

# Función principal que procesa las tareas abiertas de un plan y las actualiza según el estado de su checklist.
def process_tasks(access_token: str, plan_id: str, completed_bucket_id: str | None = None) -> None:
    """Evalúa y actualiza el estado de las tareas abiertas.

    - en curso si checklist parcialmente completado
    - completadas y movidas si checklist 100%
    """
    tasks = list_open_tasks(access_token, plan_id)
    print(f"Encontradas {len(tasks)} tareas abiertas en el plan {plan_id}")
    for t in tasks:
        print(f"-> {t['title']} ({t['id']}) status={t['status']} pct={t['percentComplete']}")
        checklist = get_task_checklist(access_token, t["id"])
        if not checklist:
            print("   - sin checklist, se omite")
            continue
        total = len(checklist)
        checked = sum(1 for c in checklist.values() if c.get("isChecked"))
        print(f"   - checklist {checked}/{total} items marcados")
        if checked == 0:
            print("   - ningún ítem marcado, no se modifica")
            continue
        if checked < total:
            pct = int(checked * 100 / total)
            print("   - parcial -> en curso")
            patch_task(access_token, t["id"], {"status": "inProgress", "percentComplete": pct})
        else:
            print("   - todos completos -> marcar completada")
            body = {"status": "completed", "percentComplete": 100}
            if completed_bucket_id:
                body["bucketId"] = completed_bucket_id
            patch_task(access_token, t["id"], body)


if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de plan: ")
    bucket_done = os.getenv("BUCKET_COMPLETADAS") or input("Id de bucket destino (completadas) (dejar vacío para no mover): ")
    bucket_done = bucket_done or None
    process_tasks(token, plan_id, bucket_done)

