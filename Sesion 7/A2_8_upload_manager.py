from datetime import datetime
import time

class UploadManager:
    """Gestor de cargas con progreso y validación."""
    
    def __init__(self, access_token, drive_id, fragment_size=262144):
        self.access_token = access_token
        self.drive_id = drive_id
        self.fragment_size = fragment_size
        self.uploads = {}
    
    def upload_file(self, folder_id, file_path, validate=True):
        """Sube archivo con validación opcional."""
        
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        # Registro
        upload_id = f"{file_name}_{int(time.time())}"
        self.uploads[upload_id] = {
            "file": file_name,
            "size": file_size,
            "start_time": datetime.now(),
            "progress": 0,
            "status": "starting"
        }
        
        try:
            if file_size <= 4 * 1024 * 1024:
                # Subida simple
                result = upload_simple(self.access_token, self.drive_id, folder_id, file_path)
            else:
                # Subida fragmentada
                result = upload_fragmented(
                    self.access_token,
                    self.drive_id,
                    folder_id,
                    file_path,
                    self.fragment_size
                )
            
            # Actualizar registro
            self.uploads[upload_id].update({
                "status": "success",
                "end_time": datetime.now(),
                "file_id": result.get("file_id")
            })
            
            return result
        
        except Exception as e:
            self.uploads[upload_id]["status"] = "failed"
            self.uploads[upload_id]["error"] = str(e)
            return {"status": "failed", "error": str(e)}
    
    def get_upload_status(self, upload_id):
        """Obtiene estado de carga."""
        
        if upload_id not in self.uploads:
            return None
        
        upload = self.uploads[upload_id]
        duration = (upload.get("end_time", datetime.now()) - upload["start_time"]).total_seconds()
        
        return {
            "file": upload["file"],
            "status": upload["status"],
            "progress": upload["progress"],
            "size": upload["size"],
            "duration": f"{duration:.1f}s",
            "speed": f"{upload['size'] / (1024**2) / max(duration, 1):.1f} MB/s" if duration else "---"
        }
    
    def get_all_uploads(self):
        """Obtiene historial de cargas."""
        
        return {
            upload_id: self.get_upload_status(upload_id)
            for upload_id in self.uploads
        }

# USO
manager = UploadManager(access_token, drive_id)

# Cargar archivo
result = manager.upload_file(folder_id, "archivo_grande.zip")

# Ver estado
status = manager.get_upload_status("archivo_grande.zip_1234567890")
print(f"Estado: {status['status']}")
print(f"Velocidad: {status['speed']}")