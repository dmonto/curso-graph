def upload_simple_validated(access_token, drive_id, folder_id, file_path):
    """Subida simple con validación de integridad."""
    
    import hashlib
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Calcular hash original
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        file_content = f.read()
        sha256_hash.update(file_content)
    
    original_hash = sha256_hash.hexdigest()
    file_name = os.path.basename(file_path)
    
    # Subir
    response = requests.put(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}:/{file_name}:/content",
        headers=headers,
        data=file_content,
        timeout=60
    )
    
    if response.status_code in [201, 200]:
        uploaded_file = response.json()
        
        # Descargar para validar
        download_url = uploaded_file.get("@microsoft.graph.downloadUrl")
        download_response = requests.get(download_url)
        
        # Calcular hash descargado
        sha256_hash = hashlib.sha256()
        sha256_hash.update(download_response.content)
        downloaded_hash = sha256_hash.hexdigest()
        
        # Validar
        if original_hash == downloaded_hash:
            return {
                "status": "success",
                "file_id": uploaded_file["id"],
                "validated": True,
                "hash": original_hash
            }
        else:
            return {
                "status": "failed",
                "error": "Hash mismatch - integridad comprometida",
                "original": original_hash,
                "downloaded": downloaded_hash
            }
    
    return {"status": "failed", "error": response.text}

# USO
result = upload_simple_validated(access_token, drive_id, folder_id, "archivo.pdf")