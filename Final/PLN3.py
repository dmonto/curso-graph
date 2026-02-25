import os
from datetime import datetime
from A1_5_list_plan_buckets import list_plan_buckets
from A1_8_list_bucket_tasks import list_bucket_tasks
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv
from A2_3_upload_simple import upload_simple

load_dotenv()

def leer_tareas_del_plan(token, plan_id):

    tareas_totales = []

    # 1) Obtener buckets del plan
    buckets = list_plan_buckets(token, plan_id)

    # 2) Para cada bucket, obtener sus tareas
    for bucket in buckets:

        bucket_id = bucket["id"]
        bucket_name = bucket["name"]

        tareas = list_bucket_tasks(token, bucket_id)

        # 3) Añadir tareas a la lista global
        for t in tareas:

            tarea = {
                "title": t.get("title"),
                "percentComplete": t.get("percentComplete", 0),
                "dueDate": t.get("dueDate"),
                "bucket": bucket_name
            }

            tareas_totales.append(tarea)

    return tareas_totales

def main():

    token = get_apponly_token()

    # LEER TAREAS DEL PLAN
    PLAN_ID = os.getenv("PLAN_ID")    
    tareas = leer_tareas_del_plan(token, PLAN_ID)

    # CALCULAR DATOS GLOBALES
    total = len(tareas)
    completadas = 0
    pendientes = 0

    for t in tareas:
        if t["percentComplete"] == 100:
            completadas += 1
        else:
            pendientes += 1

    if total > 0:
        progreso_global = round((completadas / total) * 100, 2)
    else:
        progreso_global = 0


    html = f"""
    <html>
    <head>
        <title>Reporte de Progreso</title>
    </head>
    <body>
        <h1>Estado Global del Proyecto</h1>
        <p><b>Fecha generación:</b> {datetime.now()}</p>

        <h2>Resumen</h2>
        <p>Total tareas: {total}</p>
        <p>Completadas: {completadas}</p>
        <p>Pendientes: {pendientes}</p>
        <p>% Progreso Global: {progreso_global}%</p>

        <h2>Próximas tareas</h2>
        <ul>
    """

    # Próximas tareas
    proximas_tareas = [t for t in tareas if t["percentComplete"] < 100]

    for t in proximas_tareas:
        html += f"<li>{t['title']}&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;Fecha Vencimiento: {t.get('dueDate','') or "Sin especificar"}&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;Bucket: {t.get('bucket')}&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;% Completado: {t.get('percentComplete','') or "Sin especificar"}</li>"

    html += """
        </ul>
    </body>
    </html>
    """

    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = "reporte_progreso.html"
    ruta = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte generado en:", ruta)

    # Ahora vamos a subirlo
    drive_id = os.getenv("DRIVE_ID")
    folder_id = os.getenv("FOLDER_ID")
    upload_simple(token, drive_id, folder_id, ruta)

    
if __name__ == "__main__":
    main()