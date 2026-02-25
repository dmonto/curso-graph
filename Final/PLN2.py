from Class.auth import GraphAuth
from Utils.utils import *
from config import load_settings
import json
from dotenv import load_dotenv

load_dotenv()
settings = load_settings()

if __name__ == "__main__":
    auth = GraphAuth(settings.client_id, settings.client_secret, settings.tenant_id)
    
    
    FOLDER_PATH = settings.folder_path
    
    files = get_files_folder(auth, settings.drive_id, FOLDER_PATH)
    
    if files:
        print(f"Found {len(files)} files in '{FOLDER_PATH}' folder.")
        
        json_files = get_json_files(files)
        
        if json_files:
            print(f"Found {len(json_files)} JSON files in '{FOLDER_PATH}' folder:")
            for file in json_files:
                print(f" - {file['name']} (ID: {file['id']})")
            
            
            for file in json_files:
                print(f"\n📄 Procesando: {file['name']}")
                
                try:
                    content = download_file_content(auth, settings.drive_id, file["id"])
                    data = json.loads(content)
                    
                    if validate_tasks_json(data):
                        # Crear tareas automáticamente según bucket asignado por código
                        create_tasks_from_json(auth, settings.plan_id, data)

                        move_file(auth, settings.drive_id, file["id"], settings.folder_destination)
                    else:
                        print("Invalid JSON structure. Skipping file.")
                

                except Exception as e:
                    print(f"Error processing {file['name']}: {e}")
        else:
            print("No JSON files found in folder.")
    else:
        print(f"No files found in folder '{FOLDER_PATH}'")