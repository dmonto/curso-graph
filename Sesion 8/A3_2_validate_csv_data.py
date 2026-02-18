def validate_csv_data(tasks, required_fields):
    """Valida que CSV tenga campos requeridos."""
    
    errors = []
    valid_tasks = []
    
    for i, task in enumerate(tasks, 1):
        # Validar campos requeridos
        missing = [f for f in required_fields if f not in task or not task[f]]
        
        if missing:
            errors.append(f"Fila {i}: Faltan campos {missing}")
            continue
        
        # Validar longitud de título
        if len(task['title']) > 255:
            errors.append(f"Fila {i}: Título muy largo (max 255)")
            continue
        
        # Validar prioridad
        try:
            priority = int(task.get('priority', 3))
            if priority < 0 or priority > 5:
                errors.append(f"Fila {i}: Prioridad inválida {priority}")
                continue
            task['priority'] = priority
        except ValueError:
            errors.append(f"Fila {i}: Prioridad debe ser número")
            continue
        
        valid_tasks.append(task)
    
    if errors:
        print(f"⚠ {len(errors)} errores encontrados:")
        for error in errors:
            print(f"  {error}")
    
    print(f"✓ {len(valid_tasks)}/{len(tasks)} tareas válidas")
    return valid_tasks, errors

# USO
if __name__ == "__main__":
    required_fields = ['title', 'bucket_name', 'priority']
    valid_tasks, errors = validate_csv_data(tasks, required_fields)