def subscribe_to_file_changes(drive_id, item_id):
    """Suscribirse a cambios de archivo."""
    
    subscription = client.post('/subscriptions', {
        "changeType": "updated",
        "notificationUrl": "https://myapp.com/webhook",
        "resource": f"/drives/{drive_id}/items/{item_id}",
        "expirationDateTime": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "clientState": "secret-state-123"
    })
    
    return subscription['id']

def handle_file_change(drive_id, item_id):
    """Manejar cambio de archivo."""
    
    # Obtener estado actual del archivo
    file_item = client.get(f'/drives/{drive_id}/items/{item_id}')
    
    # Obtener mensajes vinculados a este archivo
    messages = client.get(
        "/me/messages",
        params={
            "$filter": f"categories/any(c:c eq 'file-linked:{drive_id}:{item_id}')"
        }
    )
    
    # Actualizar metadatos en cada mensaje
    for message in messages['value']:
        update_message_file_metadata(
            message['id'],
            file_item,
            drive_id,
            item_id
        )
    
    return f"Updated {len(messages['value'])} messages"

def update_message_file_metadata(message_id, file_item, drive_id, item_id):
    """Actualiza metadatos del archivo en el mensaje."""
    
    client.patch(f'/me/messages/{message_id}', {
        "categories": [
            f"file-linked:{drive_id}:{item_id}",
            f"file-name:{file_item['name']}",
            f"file-modified:{file_item['lastModifiedDateTime']}"
        ]
    })