def read_json_file(filepath):
    """Lee archivo JSON y retorna lista de tareas."""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # JSON puede estar en 'tasks' o ser array directo
        tasks = data if isinstance(data, list) else data.get('tasks', [])
        
        print(f"✓ {len(tasks)} tareas leídas de JSON")
        return tasks
    
    except FileNotFoundError:
        raise Exception(f"Archivo no encontrado: {filepath}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON inválido: {e}")
    except Exception as e:
        raise Exception(f"Error leyendo JSON: {str(e)}")

# USO
if __name__ == "__main__":
    tasks = read_json_file("tareas.json")