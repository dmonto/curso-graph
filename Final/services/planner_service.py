import os

import requests


def create_task(auth, plan_id, bucket_id, title, due_date, description, priority):
    url = "https://graph.microsoft.com/v1.0/planner/tasks"

    payload = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": title,
        "dueDateTime": f"{due_date}",
        "details": {"description": description},
        "priority": priority,
    }

    response = requests.post(url, headers=auth.get_headers(), json=payload)

    if response.status_code in (200, 201):
        print(f"✅ Task created: {title}")
        return response.json()
    else:
        print(f"❌ Error creating task {title}: {response.text}")
        return None


def get_bucket_id_by_code(code):
    if code.startswith("TEST"):
        return os.getenv("BUCKET_TEST_ID")
    elif code.startswith("PREP"):
        return os.getenv("BUCKET_PRED_ID")
    elif code.startswith("PROD"):
        return os.getenv("BUCKET_PROD_ID")
    else:
        return None


def create_tasks_from_json(auth, plan_id, data):
    for code, info in data.items():
        bucket_id = get_bucket_id_by_code(code)
        if not bucket_id:
            print(f"⚠️ Código {code} no coincide con ningún bucket, se omite")
            continue

        title = code
        due_date = info["Fecha"]
        description = info["Detalle"]
        priority = {"Alta": 1, "Media": 3, "Baja": 5}.get(info["Prioridad"], 3)

        create_task(
            auth=auth,
            plan_id=plan_id,
            bucket_id=bucket_id,
            title=title,
            due_date=due_date,
            description=description,
            priority=priority,
        )
