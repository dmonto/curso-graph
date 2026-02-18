import csv

def process_csv_advanced(filepath, transformations=None):
    """Lee y procesa CSV con transformaciones."""
    
    tasks = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            task = dict(row)
            
            # Transformaciones
            if transformations:
                for key, transform_fn in transformations.items():
                    if key in task:
                        try:
                            task[key] = transform_fn(task[key])
                        except Exception as e:
                            print(f"⚠ Error transformando {key} en fila {i}: {e}")
            
            # Procesar usuarios
            if 'assigned_to' in task:
                users = [u.strip() for u in task['assigned_to'].split(',')]
                task['assigned_to'] = users
            
            # Procesar etiquetas
            if 'labels' in task:
                labels = [l.strip() for l in task['labels'].split(',')]
                task['labels'] = labels
            
            tasks.append(task)
    
    return tasks

# USO
if __name__ == "__main__":
    transformations = {
        'title': lambda x: x.strip().title(),
        'priority': int,
        'description': lambda x: x.strip() if x else ""
    }

    tasks = process_csv_advanced("tareas.csv", transformations)