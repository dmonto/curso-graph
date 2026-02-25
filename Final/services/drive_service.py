import requests


def list_root_files(auth, drive_id):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"

    response = requests.get(url, headers=auth.get_headers())

    if response.status_code != 200:
        raise Exception(response.text)

    for item in response.json()["value"]:
        graph_path = item["parentReference"]["path"]
        clean_path = graph_path.split("root:")[-1]
        full_path = f"{clean_path}/{item['name']}"
        print(f"   PATH: {full_path}")


def get_files_folder(auth, drive_id, path):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{path}:/children"
    files = []
    response = requests.get(url, headers=auth.get_headers())
    if response.status_code != 200:
        raise Exception(response.text)

    for item in response.json()["value"]:
        files.append(
            {
                "name": item["name"],
                "id": item["id"],
                "type": "folder" if "folder" in item else "file",
            }
        )
    return files


def get_json_files(files):
    json_files = []
    for file in files:
        if file["type"] == "file" and file["name"].endswith(".json"):
            json_files.append({"name": file["name"], "id": file["id"]})
    return json_files


def download_file_content(auth, drive_id, item_id):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content"

    response = requests.get(url, headers=auth.get_headers())

    if response.status_code != 200:
        raise Exception(response.text)

    return response.text

def move_file(auth, drive_id, item_id, destination_folder_path):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}"
    parent_path = f"/drive/root:/{destination_folder_path}"

    payload = {
        "parentReference": {
            "path": parent_path
        }
    }
    response = requests.patch(url, headers=auth.get_headers(), json=payload)
    if response.status_code in (200, 201):
        print(f"✅ File {item_id} moved correctly to {destination_folder_path}")
        return response.json()
    else:
        raise Exception(f"❌ Error moving file {item_id}: {response.status_code} - {response.text}")