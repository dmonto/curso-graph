def normalize_json_data(tasks):
    """Normaliza datos JSON a formato estándar."""
    
    normalized = []
    
    for task in tasks:
        norm = {
            'title': task.get('title', '').strip(),
            'bucket_name': task.get('bucket_name', ''),
            'priority': task.get('priority', 3),
            'assigned_to': task.get('assigned_to', []),
            'labels': task.get('labels', []),
            'description': task.get('description', ''),
            'percentComplete': task.get('percentComplete', 0),
            'dueDate': task.get('dueDate', None)
        }
        
        # Asegurar que assigned_to es lista
        if isinstance(norm['assigned_to'], str):
            norm['assigned_to'] = [norm['assigned_to']]
        
        # Asegurar que labels es lista
        if isinstance(norm['labels'], str):
            norm['labels'] = [norm['labels']]
        
        normalized.append(norm)
    
    return normalized

# USO
if __name__ == "__main__":
    normalized = normalize_json_data(valid_tasks)