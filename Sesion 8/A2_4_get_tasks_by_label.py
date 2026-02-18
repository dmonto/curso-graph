def get_tasks_by_label(access_token, bucket_id, label_id):
    """Obtiene tareas con una etiqueta específica."""
    
    import requests
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Listar tareas del bucket
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/planner/buckets/{bucket_id}/tasks",
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.text}")
    
    tasks = response.json().get("value", [])
    
    # Filtrar por etiqueta (requiere obtener detalles)
    filtered_tasks = []
    
    for task in tasks:
        detail_response = requests.get(
            f"https://graph.microsoft.com/v1.0/planner/tasks/{task['id']}/details",
            headers=headers,
            timeout=30
        )
        
        if detail_response.status_code == 200:
            details = detail_response.json()
            categories = details.get("appliedCategories", {})
            
            if label_id in categories and categories[label_id]:
                filtered_tasks.append({
                    "id": task.get("id"),
                    "title": task.get("title"),
                    "priority": task.get("priority"),
                    "percentComplete": task.get("percentComplete")
                })
    
    print(f"✓ {len(filtered_tasks)} tareas encontradas")
    return filtered_tasks

# USO
urgent_tasks = get_tasks_by_label(token, bucket_id, "0")  # Etiqueta "Urgente"