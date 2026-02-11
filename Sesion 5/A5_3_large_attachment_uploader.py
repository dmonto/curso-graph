from pathlib import Path
import requests
from A0_1_get_token import get_delegated_token

SCOPES = ["Mail.ReadWrite"]
token = get_delegated_token(SCOPES)

class LargeAttachmentUploader:
    """Sube anexos grandes (3-150 MB) a Outlook."""
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.chunk_size = 4 * 1024 * 1024  # 4 MB máximo
    
    def create_upload_session(self, message_id, file_path):
        """Paso 1: Crear sesión de upload."""
        file_size = Path(file_path).stat().st_size
        file_name = Path(file_path).name
        
        payload = {
            "AttachmentItem": {
                "attachmentType": "file",
                "name": file_name,
                "size": file_size
            }
        }
        
        url = f"https://graph.microsoft.com/beta/me/messages/{message_id}/attachments/createUploadSession"
        
        response = requests.post(url, headers=self.base_headers, json=payload)
        
        if response.status_code != 201:
            raise Exception(f"Error creando sesión: {response.status_code} - {response.text}")
        
        session_data = response.json()
        return {
            "uploadUrl": session_data["uploadUrl"],
            "expirationDateTime": session_data["expirationDateTime"],
            "fileSize": file_size
        }
    
    def upload_chunks(self, upload_session, file_path, on_progress=None):
        """Paso 2: Subir chunks."""
        upload_url = upload_session["uploadUrl"]
        file_size = upload_session["fileSize"]
        uploaded = 0
        
        with open(file_path, "rb") as f:
            while uploaded < file_size:
                # Leer chunk
                chunk_data = f.read(self.chunk_size)
                chunk_length = len(chunk_data)
                
                # Preparar headers para este chunk
                headers = {
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(chunk_length),
                    "Content-Range": f"bytes {uploaded}-{uploaded + chunk_length - 1}/{file_size}"
                }
                
                # Subir chunk
                response = requests.put(upload_url, headers=headers, data=chunk_data)
                
                if response.status_code not in [200, 201]:
                    raise Exception(f"Error en chunk: {response.status_code}")
                
                uploaded += chunk_length
                
                # Callback de progreso
                if on_progress:
                    percentage = (uploaded / file_size) * 100
                    on_progress(percentage, uploaded, file_size)
    
    def upload_large_attachment(self, message_id, file_path):
        """Flujo completo de upload."""
        print(f"Iniciando upload de {Path(file_path).name}...")
        
        # Paso 1: Crear sesión
        session = self.create_upload_session(message_id, file_path)
        print(f"Sesión creada. Tamaño: {session['fileSize'] / (1024*1024):.1f}MB")
        
        # Paso 2: Subir chunks
        def progress_callback(percent, uploaded, total):
            mb_uploaded = uploaded / (1024 * 1024)
            mb_total = total / (1024 * 1024)
            print(f"Progreso: {percent:.1f}% ({mb_uploaded:.1f}MB / {mb_total:.1f}MB)")
        
        self.upload_chunks(session, file_path, on_progress=progress_callback)
        
        print("Upload completado!")
        return True

# Uso
uploader = LargeAttachmentUploader(token)
uploader.upload_large_attachment("message-id", "archivo_grande.zip")