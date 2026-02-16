def link_message_to_file(message_id, drive_id, item_id):
    """Vincula un mensaje a un archivo de SharePoint/OneDrive."""
    
    # Obtener mensaje
    message = client.get(f'/me/messages/{message_id}')
    
    # Obtener archivo
    file_item = client.get(f'/drives/{drive_id}/items/{item_id}')
    
    # Crear vinculación (almacenar en categorías del mensaje)
    update_data = {
        "categories": [
            f"file-linked:{drive_id}:{item_id}",
            f"file-name:{file_item['name']}"
        ]
    }
    
    client.patch(f'/me/messages/{message_id}', update_data)
    
    # También crear referencia en mensaje (body update)
    link_html = f"""
    <p>
        <strong>Archivo vinculado:</strong> 
        <a href="{file_item['webUrl']}">{file_item['name']}</a>
        <br/>
        <small>Tamaño: {file_item['size']} bytes | 
        Modificado: {file_item['lastModifiedDateTime']}</small>
    </p>
    """
    
    client.patch(
        f'/me/messages/{message_id}',
        {
            "body": {
                "contentType": "html",
                "content": message['body']['content'] + link_html
            }
        }
    )
    
    return {
        "message_id": message_id,
        "file_id": item_id,
        "file_name": file_item['name'],
        "file_url": file_item['webUrl'],
        "linked_at": datetime.utcnow().isoformat()
    }

# USO
result = link_message_to_file(
    message_id="AAMkADE4...",
    drive_id="b!ABCdef",
    item_id="01ABCD"
)