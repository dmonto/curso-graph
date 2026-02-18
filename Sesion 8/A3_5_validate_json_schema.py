def validate_json_schema(tasks):
    """Valida schema de tareas JSON."""
    
    required_fields = ['title', 'bucket_name', 'priority']
    errors = []
    valid_tasks = []
    
    for i, task in enumerate(tasks, 1):
        # Validar tipo
        if not isinstance(task, dict):
            errors.append(f"Tarea {i}: Debe ser objeto")
            continue
        
        # Validar campos
        missing = [f for f in required_fields if f not in task]
        if missing:
            errors.append(f"Tarea {i}: Faltan {missing}")
            continue
        
        # Validar types
        if not isinstance(task['title'], str):
            errors.append(f"Tarea {i}: title debe ser string")
            continue
        
        if not isinstance(task['priority'], int):
            errors.append(f"Tarea {i}: priority debe ser int")
            continue
        
        if 'assigned_to' in task and not isinstance(task.get('assigned_to'), list):
            errors.append(f"Tarea {i}: assigned_to debe ser array")
            continue
        
        valid_tasks.append(task)
    
    if errors:
        print(f"⚠ {len(errors)} errores:")
        for error in errors:
            print(f"  {error}")
    
    print(f"✓ {len(valid_tasks)}/{len(tasks)} válidas")
    return valid_tasks, errors

# USO
if __name__ == "__main__":
    valid_tasks, errors = validate_json_schema(tasks)