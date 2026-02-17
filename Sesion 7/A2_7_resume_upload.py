def resume_upload(access_token, upload_url, file_path, fragment_size=262144):
    """Reanuda una carga interrumpida."""
    
    file_size = os.path.getsize(file_path)
    
    # 1. Obtener estado actual
    status_response = requests.put(
        upload_url,
        headers={"Content-Length": "0", "Content-Range": f"bytes */{file_size}"},
        timeout=60
    )
    
    if status_response.status_code == 202:
        # Sesión activa, obtener rangos pendientes
        next_ranges = status_response.json().get("nextExpectedRanges", [])
        
        # 2. Cargar fragmentos pendientes
        with open(file_path, 'rb') as f:
            for range_str in next_ranges:
                start, end = map(int, range_str.split('-'))
                
                # Ir a posición
                f.seek(start)
                
                # Leer fragmento
                chunk = f.read(end - start + 1)
                
                # Subir
                headers = {
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {start}-{end}/{file_size}"
                }
                
                response = requests.put(upload_url, headers=headers, data=chunk, timeout=300)
                
                if response.status_code not in [200, 201]:
                    return {"status": "failed", "error": f"Error en rango {range_str}"}
        
        return {"status": "success", "resumed": True}
    
    elif status_response.status_code == 201:
        # Carga completada
        return {"status": "success", "completed": True}
    
    return {"status": "failed", "error": status_response.text}

# USO
result = resume_upload(access_token, upload_url, "archivo_grande.zip")