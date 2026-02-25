import json

from jsonschema import FormatChecker, ValidationError, validate

from services.drive_service import download_file_content


def process_json_files(auth, drive_id, json_files):
    for file in json_files:
        print(f"\n📄 Procesando: {file['name']}")

        try:
            content = download_file_content(auth, drive_id, file["id"])

            data = json.loads(content)

            is_valid = validate_tasks_json(data)

            if is_valid:
                print("Archivo listo para crear tareas")
            else:
                print("Archivo inválido, no se utilizará para crear tareas")

        except Exception as e:
            print(f"❌ Error procesando {file['name']}: {e}")


def validate_tasks_json(data):
    metadata_schema = {
        "type": "object",
        "patternProperties": {
            "^[A-Z]+-[0-9]+$": {
                "type": "object",
                "required": ["Detalle", "Fecha", "Prioridad"],
                "properties": {
                    "Detalle": {"type": "string", "minLength": 1},
                    "Fecha": {"type": "string", "format": "date"},
                    "Prioridad": {
                        "type": "string",
                        "enum": ["Alta", "Media", "Baja"],
                    },
                },
                "additionalProperties": False,
            }
        },
        "additionalProperties": False,
    }

    try:
        validate(instance=data, schema=metadata_schema, format_checker=FormatChecker())
        print("✅ JSON válido")
        return True
    except ValidationError as e:
        print("❌ JSON inválido:")
        print(e.message)
        return False
