import requests
import os
from A0_1_get_token import get_apponly_token
from dotenv import load_dotenv
from A3_1_create_folder import create_folder

load_dotenv()

def create_folder_structure(access_token, drive_id, parent_id, folder_structure):
    """Crea estructura jerárquica de carpetas."""
    
    results = []
    
    def create_recursive(parent_item_id, structure):
        for folder_info in structure:
            folder_name = folder_info["name"]
            subfolders = folder_info.get("children", [])
            
            # Crear carpeta
            result = create_folder(access_token, drive_id, parent_item_id, folder_name)
            
            if result["status"] == "success":
                results.append(result)
                
                # Crear subcarpetas
                if subfolders:
                    create_recursive(result["id"], subfolders)
    
    create_recursive(parent_id, folder_structure)
    return results

# USO
structure = [
    {
        "name": "Proyectos",
        "children": [
            {"name": "2026", "children": [
                {"name": "Q1"},
                {"name": "Q2"}
            ]},
            {"name": "2025"}
        ]
    },
    {"name": "Documentos"},
    {"name": "Archivos"}
]

token = get_apponly_token()
drive_id = os.getenv("DRIVE_ID") or input("Id de Drive:")
folder_id = os.getenv("FOLDER_ID") or input("Id de Folder Padre:")
results = create_folder_structure(token, drive_id, folder_id, structure)
print(f"Carpetas creadas: {len(results)}")