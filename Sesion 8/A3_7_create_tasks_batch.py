def create_tasks_batch(token, plan_id, bucket_map, tasks):
    """Crea tareas en lote."""
    
    import requests
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    results = {
        'success': 0,
        'failed': 0,
        'errors': []
    }
    
    for task in tasks:
        try:
            # Obtener bucket ID
            bucket_name = task.get('bucket_name', '')
            if bucket_name not in bucket_map:
                results['errors'].append(f"{task['title']}: Bucket '{bucket_name}' no existe")
                results['failed'] += 1
                continue
            
            bucket_id = bucket_map[bucket_name]
            
            # Procesar asignaciones
            assignments = {}
            for email in task.get('assigned_to', []):
                if email.strip():
                    assignments[email.strip()] = {
                        "@odata.type": "#microsoft.graph.plannerAssignment"
                    }
            
            # Crear tarea
            payload = {
                "planId": plan_id,
                "bucketId": bucket_id,
                "title": task['title'],
            }
            
            if task.get('description'):
                payload['description'] = task['description']
            
            r = requests.post(
                "https://graph.microsoft.com/v1.0/planner/tasks",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if r.status_code == 201:
                results['success'] += 1
                print(f"✓ {task['title']}")
            else:
                results['failed'] += 1
                results['errors'].append(f"{task['title']}: {r.text}")
        
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{task['title']}: {str(e)}")
    
    return results

# USO
if __name__ == "__main__":
    results = create_tasks_batch(token, plan_id, bucket_map, valid_tasks)
    print(f"Éxito: {results['success']}, Fallido: {results['failed']}")