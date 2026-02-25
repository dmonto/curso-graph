import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv
import datetime
import html
from A1_5_list_plan_buckets import list_plan_buckets
from A1_8_list_bucket_tasks import list_bucket_tasks

load_dotenv()

def safe_dt(dt_str):
    """Parsea una fecha de Graph de forma segura."""
    if not dt_str:
        return "—"
    try:
        # Quitar Z final si existe (Graph la usa)
        dt_str = dt_str.rstrip("Z")
        # Intentar parsear con segundos
        try:
            dt = datetime.datetime.fromisoformat(dt_str)
        except ValueError:
            # Intentar sin hora
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "—"

def get_user_info(access_token, user_id, cache):
    """Obtiene información básica de un usuario con caché."""
    if user_id in cache:
        return cache[user_id]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}",
        headers=headers,
        timeout=30
    )
    if response.status_code == 200:
        name = response.json().get("displayName", user_id)
        cache[user_id] = name
        return name
    return user_id

def build_html(plan_title: str, buckets: list, tasks_by_bucket: dict, user_names: dict) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    css = """
    body { font-family: Arial, sans-serif; margin: 24px; color: #111; }
    h1 { margin-bottom: 6px; }
    .meta { color: #555; margin-bottom: 18px; }
    .bucket { margin-top: 22px; padding-top: 10px; border-top: 1px solid #ddd; }
    .bucket h2 { margin: 0 0 10px 0; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #e1e1e1; padding: 8px; vertical-align: top; }
    th { background: #f6f6f6; text-align: left; }
    .small { color: #666; font-size: 12px; }
    .pill { display:inline-block; padding:2px 8px; border-radius:999px; background:#eee; font-size:12px; }
    """

    out = []
    out.append("<!doctype html>")
    out.append("<html><head><meta charset='utf-8'>")
    out.append(f"<title>{html.escape(plan_title)} - Export</title>")
    out.append(f"<style>{css}</style></head><body>")
    out.append(f"<h1>{html.escape(plan_title)}</h1>")
    out.append(f"<div class='meta'>Generado: {html.escape(now)}</div>")

    # buckets es UNA LISTA → corregido
    for b in sorted(buckets, key=lambda x: (x.get("name") or "").lower()):
        bucket_id = b.get("id")
        bucket_name = b.get("name", "Sin bucket")

        out.append("<div class='bucket'>")
        out.append(f"<h2>{html.escape(bucket_name)}</h2>")

        tasks = tasks_by_bucket.get(bucket_id, [])
        if not tasks:
            out.append("<div class='small'>No hay tareas.</div>")
            out.append("</div>")
            continue

        def due_key(t):
            d = t.get("dueDateTime")
            return (d is None, d or "")

        tasks = sorted(tasks, key=due_key)

        out.append("<table>")
        out.append("<tr><th>Tarea</th><th>Estado</th><th>Vence</th><th>Asignado</th><th>Prioridad</th></tr>")

        for t in tasks:
            title = t.get("title", "")
            percent = t.get("percentComplete", 0)
            status = "Completada" if percent == 100 else ("En progreso" if percent > 0 else "Pendiente")
            due = safe_dt(t.get("dueDateTime"))
            assignees = t.get("assignments", {})

            # A partir de assignments, obtener los nombres de todos los usuarios asignados
            if assignees:
                names_list = []
                for uid in assignees.keys():
                    names_list.append(user_names.get(uid, uid))
                assignee_name = ", ".join(names_list)
            else:
                assignee_name = "Sin asignación"

            priority_val = t.get("priority", "—")

            out.append("<tr>")
            out.append(f"<td>{html.escape(title)}</td>")
            out.append(f"<td><span class='pill'>{html.escape(status)}</span> <span class='small'>({percent}%)</span></td>")
            out.append(f"<td>{html.escape(due)}</td>")
            out.append(f"<td>{html.escape(str(assignee_name))}</td>")
            out.append(f"<td>{html.escape(str(priority_val))}</td>")
            out.append("</tr>")

        out.append("</table>")
        out.append("</div>")

    out.append("</body></html>")
    return "\n".join(out)

def get_plan(access_token, plan_id):
    """Obtiene detalles de un plan."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        plan = response.json()
        # print(plan)
        return {
            "id": plan.get("id"),
            "title": plan.get("title"),
            "owner": plan.get("owner"),
            "created": plan.get("createdDateTime"),
            "modified": plan.get("modifiedDateTime")
        }
    else:
        raise Exception(f"Error: {response.text}")

if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")
    plan_info = get_plan(token, plan_id)

    # Llamar a build_html con los datos del plan
    buckets = list_plan_buckets(token, plan_id)
    tasks_by_bucket = {}
    user_cache = {}
    
    print("Recuperando tareas y usuarios...")
    for bucket in buckets:
        tasks = list_bucket_tasks(token, bucket['id'])
        tasks_by_bucket[bucket['id']] = tasks
        for t in tasks:
            assignments = t.get("assignments", {})
            for uid in assignments:
                get_user_info(token, uid, user_cache)
                
    html_content = build_html(plan_info['title'], buckets, tasks_by_bucket, user_cache)
    filename = f"reporte_plan_{plan_info['title'].replace(' ', '_')}.html"  
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)    
    print(html_content)