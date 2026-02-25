import requests
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from A0_1_get_token import get_apponly_token
from A0_1_get_delegated_token import get_delegated_token

load_dotenv()

GRAPH_URL = "https://graph.microsoft.com/v1.0"
SNAPSHOT_FILE = "task_snapshot.json"

# Mapeo de valores numericos de prioridad a etiquetas legibles
PRIORITY_LABELS = {
    0: "Urgente",
    1: "Urgente",
    2: "Importante",
    3: "Media",
    4: "Media",
    5: "Baja",
    6: "Baja",
    7: "Baja",
    8: "Baja",
    9: "Baja",
}

# Mapeo de porcentaje de progreso a etiquetas legibles
PROGRESS_LABELS = {
    0: "No iniciada",
    50: "En curso",
    100: "Completada",
}

# Etiquetas de los campos monitorizados para los mensajes
FIELD_LABELS = {
    "nueva": "Nueva tarea",
    "deposito": "Deposito",
    "progreso": "Progreso",
    "prioridad": "Prioridad",
    "vencimiento": "Vencimiento",
}


# ---------------------------------------------------------------------------
# Funciones de Graph API
# ---------------------------------------------------------------------------

def get_plan(token, plan_id):
    """Obtiene detalles del plan. El campo 'owner' es el ID del grupo
    propietario, que coincide con el ID del equipo de Teams."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"{GRAPH_URL}/planner/plans/{plan_id}",
        headers=headers,
        timeout=30,
    )
    if r.status_code == 200:
        return r.json()
    raise Exception(f"Error obteniendo plan: {r.text}")


def get_plan_buckets(token, plan_id):
    """Obtiene los buckets del plan. Devuelve dict {bucket_id: nombre}."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"{GRAPH_URL}/planner/plans/{plan_id}/buckets",
        headers=headers,
        timeout=30,
    )
    if r.status_code == 200:
        return {b["id"]: b["name"] for b in r.json().get("value", [])}
    raise Exception(f"Error obteniendo buckets: {r.text}")


def get_plan_tasks(token, plan_id):
    """Obtiene todas las tareas del plan."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"{GRAPH_URL}/planner/plans/{plan_id}/tasks",
        headers=headers,
        timeout=30,
    )
    if r.status_code == 200:
        tasks = r.json().get("value", [])
        print(f"{len(tasks)} tareas obtenidas")
        return tasks
    raise Exception(f"Error obteniendo tareas: {r.text}")


def get_team_channels(token, team_id):
    """Obtiene los canales del equipo. Devuelve dict {nombre: channel_id}."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"{GRAPH_URL}/teams/{team_id}/channels",
        headers=headers,
        params={"$select": "id,displayName"},
        timeout=30,
    )
    if r.status_code == 200:
        return {ch["displayName"]: ch["id"] for ch in r.json().get("value", [])}
    raise Exception(f"Error obteniendo canales: {r.text}")


def send_channel_message(token, team_id, channel_id, html_content):
    """Envia un mensaje HTML a un canal de Teams."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "body": {
            "contentType": "html",
            "content": html_content,
        }
    }
    r = requests.post(
        f"{GRAPH_URL}/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if r.status_code == 201:
        return r.json().get("id")
    raise Exception(f"Error enviando mensaje: {r.text}")


# ---------------------------------------------------------------------------
# Gestion de snapshot
# ---------------------------------------------------------------------------

def _snapshot_path():
    """Devuelve la ruta absoluta del fichero de snapshot en el directorio
    del script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, SNAPSHOT_FILE)


def load_snapshot():
    """Carga el snapshot anterior. Si no existe, devuelve estructura vacia."""
    path = _snapshot_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": {}}


def save_snapshot(tasks):
    """Guarda el snapshot actual a disco."""
    path = _snapshot_path()
    data = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "tasks": {},
    }
    for task in tasks:
        data["tasks"][task["id"]] = {
            "title": task.get("title", ""),
            "bucketId": task.get("bucketId", ""),
            "percentComplete": task.get("percentComplete", 0),
            "priority": task.get("priority", 5),
            "dueDateTime": task.get("dueDateTime"),
        }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Snapshot guardado: {path}")


# ---------------------------------------------------------------------------
# Deteccion de cambios
# ---------------------------------------------------------------------------

def detect_changes(current_tasks, previous_snapshot, bucket_names):
    """Compara el estado actual de las tareas con el snapshot anterior.
    Devuelve una lista de diccionarios con los cambios detectados."""
    previous_tasks = previous_snapshot.get("tasks", {})
    changes = []

    for task in current_tasks:
        task_id = task["id"]
        title = task.get("title", "Sin titulo")

        # Tarea nueva: notificar creacion
        if task_id not in previous_tasks:
            bucket_name = bucket_names.get(task.get("bucketId"), "Sin bucket")
            priority_label = PRIORITY_LABELS.get(task.get("priority", 5), "Media")
            due = task.get("dueDateTime")
            due_str = due[:10] if due else "Sin fecha"
            changes.append({
                "task_id": task_id,
                "title": title,
                "bucketId": task.get("bucketId"),
                "field": "nueva",
                "old_value": "-",
                "new_value": f"Bucket: {bucket_name} | Prioridad: {priority_label} | Vencimiento: {due_str}",
            })
            continue

        prev = previous_tasks[task_id]

        # -- Deposito (bucket) --
        if task.get("bucketId") != prev.get("bucketId"):
            old_name = bucket_names.get(prev.get("bucketId"), "Desconocido")
            new_name = bucket_names.get(task.get("bucketId"), "Desconocido")
            changes.append({
                "task_id": task_id,
                "title": title,
                "bucketId": task.get("bucketId"),
                "field": "deposito",
                "old_value": old_name,
                "new_value": new_name,
            })

        # -- Progreso --
        if task.get("percentComplete") != prev.get("percentComplete"):
            old_pct = prev.get("percentComplete", 0)
            new_pct = task.get("percentComplete", 0)
            old_label = PROGRESS_LABELS.get(old_pct, str(old_pct))
            new_label = PROGRESS_LABELS.get(new_pct, str(new_pct))
            changes.append({
                "task_id": task_id,
                "title": title,
                "bucketId": task.get("bucketId"),
                "field": "progreso",
                "old_value": f"{old_label} ({old_pct}%)",
                "new_value": f"{new_label} ({new_pct}%)",
            })

        # -- Prioridad --
        if task.get("priority") != prev.get("priority"):
            old_label = PRIORITY_LABELS.get(prev.get("priority", 5), "Desconocida")
            new_label = PRIORITY_LABELS.get(task.get("priority", 5), "Desconocida")
            changes.append({
                "task_id": task_id,
                "title": title,
                "bucketId": task.get("bucketId"),
                "field": "prioridad",
                "old_value": old_label,
                "new_value": new_label,
            })

        # -- Vencimiento --
        if task.get("dueDateTime") != prev.get("dueDateTime"):
            old_due = prev.get("dueDateTime") or "Sin fecha"
            new_due = task.get("dueDateTime") or "Sin fecha"
            if old_due != "Sin fecha":
                old_due = old_due[:10]
            if new_due != "Sin fecha":
                new_due = new_due[:10]
            changes.append({
                "task_id": task_id,
                "title": title,
                "bucketId": task.get("bucketId"),
                "field": "vencimiento",
                "old_value": old_due,
                "new_value": new_due,
            })

    return changes


# ---------------------------------------------------------------------------
# Formato de mensajes
# ---------------------------------------------------------------------------

def format_change_html(change):
    """Genera el fragmento HTML para un cambio individual."""
    label = FIELD_LABELS.get(change["field"], change["field"])
    if change["field"] == "nueva":
        return (
            f"<b>{label}:</b> {change['title']}<br>"
            f"<b>Detalles:</b> {change['new_value']}"
        )
    return (
        f"<b>Tarea:</b> {change['title']}<br>"
        f"<b>Campo:</b> {label}<br>"
        f"<b>Anterior:</b> {change['old_value']}<br>"
        f"<b>Nuevo:</b> {change['new_value']}"
    )


def build_consolidated_message(plan_title, changes_list):
    """Construye un unico mensaje HTML con todos los cambios destinados
    a un mismo canal, agrupados por tarea."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [
        f"<h3>Cambios detectados en plan: {plan_title}</h3>",
        f"<p><i>{timestamp}</i></p><hr>",
    ]

    # Agrupar cambios por tarea manteniendo orden de aparicion
    tasks_order = []
    tasks_changes = {}
    for change in changes_list:
        tid = change["task_id"]
        if tid not in tasks_changes:
            tasks_order.append(tid)
            tasks_changes[tid] = {
                "title": change["title"],
                "is_new": False,
                "new_detail": "",
                "fields": [],
            }
        if change["field"] == "nueva":
            tasks_changes[tid]["is_new"] = True
            tasks_changes[tid]["new_detail"] = change["new_value"]
        else:
            label = FIELD_LABELS.get(change["field"], change["field"])
            tasks_changes[tid]["fields"].append({
                "label": label,
                "old": change["old_value"],
                "new": change["new_value"],
            })

    for tid in tasks_order:
        info = tasks_changes[tid]
        if info["is_new"]:
            parts.append(
                f"<b>Nueva tarea:</b> {info['title']}<br>"
                f"<b>Detalles:</b> {info['new_detail']}"
            )
        else:
            parts.append(f"<b>Tarea:</b> {info['title']}")
            for field in info["fields"]:
                parts.append(
                    f"<b>{field['label']}:</b> {field['old']} -> {field['new']}"
                )
        parts.append("<hr>")

    return "<br>".join(parts)


# ---------------------------------------------------------------------------
# Resolucion de canal correspondiente
# ---------------------------------------------------------------------------

def resolve_channel(change, bucket_names, channel_map, default_channel_id):
    """Busca un canal cuyo nombre coincida con el nombre del bucket de la
    tarea. Si no hay coincidencia, devuelve el canal por defecto (General)."""
    bucket_name = bucket_names.get(change.get("bucketId"), "")
    if bucket_name in channel_map:
        return channel_map[bucket_name]
    return default_channel_id


# ---------------------------------------------------------------------------
# Ejecucion principal
# ---------------------------------------------------------------------------

def main():
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("ID del Plan: ")

    # 1. Obtener datos del plan
    plan = get_plan(token, plan_id)
    team_id = plan["owner"]  # El grupo propietario coincide con el equipo
    plan_title = plan.get("title", "")
    print(f"Plan: {plan_title} (Equipo: {team_id})")

    # 2. Obtener buckets y canales
    bucket_names = get_plan_buckets(token, plan_id)
    print(f"{len(bucket_names)} buckets obtenidos")

    channel_map = get_team_channels(token, team_id)
    print(f"{len(channel_map)} canales obtenidos")

    # Canal por defecto: General, o el primero disponible
    default_channel_id = channel_map.get("General")
    if not default_channel_id:
        default_channel_id = next(iter(channel_map.values()), None)
    if not default_channel_id:
        raise Exception("No se encontraron canales en el equipo")

    # 3. Obtener tareas actuales
    current_tasks = get_plan_tasks(token, plan_id)

    # 4. Cargar snapshot anterior
    previous_snapshot = load_snapshot()
    is_first_run = not previous_snapshot.get("tasks")

    if is_first_run:
        print("Primera ejecucion: se genera snapshot inicial sin notificaciones")
        save_snapshot(current_tasks)
        return

    # 5. Detectar cambios
    changes = detect_changes(current_tasks, previous_snapshot, bucket_names)

    if not changes:
        print("Sin cambios detectados")
        save_snapshot(current_tasks)
        return

    print(f"{len(changes)} cambios detectados")

    # 6. Agrupar cambios por canal para enviar un unico mensaje por canal
    changes_by_channel = {}
    for change in changes:
        channel_id = resolve_channel(
            change, bucket_names, channel_map, default_channel_id
        )
        if channel_id not in changes_by_channel:
            changes_by_channel[channel_id] = []
        changes_by_channel[channel_id].append(change)

    # 7. Obtener token delegado para enviar mensajes a canales
    delegated_token = get_delegated_token(["ChannelMessage.Send"])

    # 8. Enviar notificaciones
    all_sent = True
    for channel_id, channel_changes in changes_by_channel.items():
        html = build_consolidated_message(plan_title, channel_changes)
        try:
            msg_id = send_channel_message(delegated_token, team_id, channel_id, html)
            print(f"Mensaje enviado al canal {channel_id}: {msg_id}")
        except Exception as e:
            print(f"Error enviando al canal {channel_id}: {e}")
            all_sent = False

    # 9. Guardar snapshot solo si todos los mensajes se enviaron correctamente
    if all_sent:
        save_snapshot(current_tasks)
    else:
        print("Snapshot NO actualizado: hubo errores en el envio de mensajes")


if __name__ == "__main__":
    main()
