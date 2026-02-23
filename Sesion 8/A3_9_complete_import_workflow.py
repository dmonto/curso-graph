import requests
import os
from A0_1_get_token import get_apponly_token
from A1_5_list_plan_buckets import list_plan_buckets
from A3_1_read_csv_file import read_csv_file
from A3_2_validate_csv_data import validate_csv_data
from A3_3_process_csv_advanced import process_csv_advanced
from A3_7_create_tasks_batch import create_tasks_batch
from A3_8_generate_import_report import generate_import_report
from dotenv import load_dotenv

load_dotenv()

def complete_import_workflow(token, plan_id, bucket_map, label_map, csv_file):
    """Flujo completo de importación."""
    
    print("=== IMPORTACIÓN MASIVA DE TAREAS ===\n")
    
    # 1. Leer datos
    print(f"1. Leyendo {csv_file}...")
    tasks = read_csv_file(csv_file)
    print(f"   ✓ {len(tasks)} tareas leídas")
    
    # 2. Validar
    print("2. Validando datos...")
    valid_tasks = validate_csv_data(tasks, required_fields=["title","bucket_name","description"])
    print(f"   ✓ {len(valid_tasks)} tareas válidas")
    
    # 3. Importar
    print("3. Importando tareas...")
    tasks = process_csv_advanced(csv_file)
    results = create_tasks_batch(token, plan_id, bucket_map, tasks)
    
    # 4. Reporte
    generate_import_report(results)
    
    return results

# USO
token = get_apponly_token()
plan_id = os.getenv("PLAN_ID") or input("Id de Plan:")

bucket_map = {"Desarrollo": "p3MU84E0GUKbVoTKzoSDY5gAJjbR", "Testing": "IT9AyBehiEqDpqhx9dVz5ZgAAAea"}
label_map = {
    "Crítico": "0",
    "Alto": "1",
    "Backend": "2",
    "Frontend": "3"
}

results = complete_import_workflow(
    token, plan_id, bucket_map, label_map,
    "tareas.csv"
)