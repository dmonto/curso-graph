import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv
import datetime
import html
from A1_8_list_bucket_tasks import list_plan_buckets
from A1_8_list_bucket_tasks import list_bucket_tasks

load_dotenv()

def safe_dt(dt_str):
    """Parsea una fecha de Graph de forma segura."""
    if not dt_str:
        return "—"
    try:
        dt_str = dt_str.rstrip("Z")
        try:
            dt = datetime.datetime.fromisoformat(dt_str)
        except ValueError:
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return "—"

def build_unassigned_report_html(plan_title: str, tasks: list) -> str:
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    css = """
    body { font-family: 'Segoe UI', sans-serif; margin: 40px; color: #333; background-color: #f4f7f9; }
    .container { max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    h1 { color: #d83b01; margin-bottom: 5px; border-bottom: 2px solid #d83b01; padding-bottom: 10px; }
    .meta { color: #777; margin-bottom: 20px; font-size: 0.85em; }
    .info-box { background-color: #fff4ce; padding: 10px 15px; border-left: 4px solid #ffb900; margin-bottom: 20px; font-size: 0.9em; }
    table { border-collapse: collapse; width: 100%; margin-top: 10px; }
    th, td { border: 1px solid #eee; padding: 12px; text-align: left; }
    th { background-color: #fdfdfd; color: #555; font-weight: 600; text-transform: uppercase; font-size: 0.8em; letter-spacing: 1px; }
    tr:nth-child(even) { background-color: #fafafa; }
    .status-badge { background-color: #dff6dd; color: #107c10; padding: 4px 8px; border-radius: 4px; font-size: 0.75em; font-weight: bold; }
    .no-results { text-align: center; padding: 40px; color: #999; font-style: italic; }
    """

    out = []
    out.append("<!doctype html>")
    out.append("<html><head><meta charset='utf-8'>")
    out.append(f"<title>Reporte Crítico: {html.escape(plan_title)}</title>")
    out.append(f"<style>{css}</style></head><body>")
    
    out.append("<div class='container'>")
    out.append(f"<h1>Tareas Completadas Sin Responsable</h1>")
    out.append(f"<div class='meta'>Plan: <b>{html.escape(plan_title)}</b> | Generado: {html.escape(now)}</div>")
    
    out.append("<div class='info-box'>Este reporte muestra únicamente las tareas que están marcadas al 100% pero no tienen ninguna persona asignada.</div>")

    if not tasks:
        out.append("<div class='no-results'>No se encontraron tareas completadas sin responsable. ¡Excelente trabajo de gestión!</div>")
    else:
        out.append("<table>")
        out.append("<tr><th>Nombre de la Tarea</th><th>Fecha Vencimiento</th><th>Estado</th></tr>")

        for t in tasks:
            title = t.get("title", "Sin título")
            due = safe_dt(t.get("dueDateTime"))
            
            out.append("<tr>")
            out.append(f"<td><b>{html.escape(title)}</b></td>")
            out.append(f"<td>{html.escape(due)}</td>")
            out.append(f"<td><span class='status-badge'>COMPLETADA</span></td>")
            out.append("</tr>")

        out.append("</table>")
        out.append(f"<div class='meta' style='margin-top:20px'>Total de incidencias: {len(tasks)}</div>")

    out.append("</div>") 
    out.append("</body></html>")
    return "\n".join(out)

def get_plan_title(access_token, plan_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}", headers=headers, timeout=20)
    if resp.status_code == 200:
        return resp.json().get("title", "Plan Desconocido")
    return "Plan Desconocido"

if __name__ == "__main__":
    token = get_apponly_token()
    plan_id = os.getenv("PLAN_ID") or input("Id de Plan: ")
    
    print(f"Buscando tareas en el plan...")
    plan_title = get_plan_title(token, plan_id)
    buckets = list_plan_buckets(token, plan_id)
    
    filtered_tasks = []
    
    for bucket in buckets:
        tasks = list_bucket_tasks(token, bucket['id'])
        for t in tasks:
            percent = t.get("percentComplete", 0)
            assignments = t.get("assignments", {})
            
            # FILTRO: Completada (100) Y SIN asignados
            if percent == 100 and not assignments:
                filtered_tasks.append(t)
    
    html_content = build_unassigned_report_html(plan_title, filtered_tasks)
    
    # Guardar reporte
    filename = "reporte_completadas_sin_responsable.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n✓ Reporte generado: {os.path.abspath(filename)}")
    print(f"✓ Tareas encontradas: {len(filtered_tasks)}")