import csv
import json

def read_csv_file(filepath):
    """Lee archivo CSV y retorna lista de tareas."""
    
    tasks = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                tasks.append(dict(row))
        
        print(f"✓ {len(tasks)} tareas leídas de CSV")
        return tasks
    
    except FileNotFoundError:
        raise Exception(f"Archivo no encontrado: {filepath}")
    except Exception as e:
        raise Exception(f"Error leyendo CSV: {str(e)}")

# USO
if __name__ == "__main__":
    tasks = read_csv_file("tareas.csv")
    for task in tasks:
        print(f"  - {task['title']}")