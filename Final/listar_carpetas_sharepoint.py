import argparse
import os
from collections import deque
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
DEFAULT_SITE_NAME = "Curso de Graph"
DEFAULT_SITE_URL = "https://cursograph.sharepoint.com/sites/GRUPOFUERTES-ELPOZOCURSO"
SCOPE = "https://graph.microsoft.com/.default"


def build_credential() -> ClientSecretCredential:
    load_dotenv()
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID_APPONLY")
    client_secret = os.getenv("CLIENT_SECRET")

    if not tenant_id or not client_id or not client_secret:
        raise RuntimeError(
            "Faltan TENANT_ID, CLIENT_ID_APPONLY o CLIENT_SECRET en .env para autenticacion app-only."
        )

    return ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )


def get_token(credential: ClientSecretCredential) -> str:
    return credential.get_token(SCOPE).token


def graph_get(url: str, token: str, params: Optional[Dict[str, str]] = None) -> Dict:
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Graph error {response.status_code}: {response.text}")
    return response.json()


def get_site_by_url(site_url: str, token: str) -> Dict:
    parsed = urlparse(site_url)
    if not parsed.netloc or not parsed.path:
        raise RuntimeError(f"URL de sitio no valida: {site_url}")

    site_path = parsed.path.rstrip("/")
    if not site_path:
        raise RuntimeError(f"La URL no contiene ruta de sitio: {site_url}")

    endpoint = f"{GRAPH_BASE}/sites/{parsed.netloc}:{site_path}"
    return graph_get(endpoint, token)


def search_site(site_name: str, token: str) -> Dict:
    data = graph_get(f"{GRAPH_BASE}/sites", token, params={"search": site_name})
    sites = data.get("value", [])

    if not sites:
        raise RuntimeError(f"No se encontro ningun sitio con search='{site_name}'.")

    exact = [s for s in sites if (s.get("displayName") or "").strip().lower() == site_name.strip().lower()]
    return exact[0] if exact else sites[0]


def get_default_drive(site_id: str, token: str) -> Dict:
    return graph_get(f"{GRAPH_BASE}/sites/{site_id}/drive", token)


def parse_parent_path(parent_path: str) -> str:
    marker = "root:/"
    if marker in parent_path:
        return parent_path.split(marker, 1)[1].strip("/")
    return ""


def list_folders(site_id: str, drive_id: str, token: str) -> List[Tuple[str, str]]:
    folders: List[Tuple[str, str]] = []
    queue: deque[str] = deque(["root"])

    while queue:
        item_id = queue.popleft()
        next_url = f"{GRAPH_BASE}/sites/{site_id}/drives/{drive_id}/items/{item_id}/children"
        params = {"$select": "id,name,folder,parentReference"}

        while next_url:
            data = graph_get(next_url, token, params=params)
            params = None

            for child in data.get("value", []):
                if "folder" not in child:
                    continue

                name = child.get("name", "")
                folder_id = child.get("id", "")
                parent_ref = child.get("parentReference", {})
                parent_graph_path = parse_parent_path(parent_ref.get("path", ""))

                full_path = "/".join(p for p in [parent_graph_path, name] if p).strip("/")
                if not full_path:
                    full_path = "/"

                folders.append((full_path, folder_id))
                queue.append(folder_id)

            next_url = data.get("@odata.nextLink")

    folders.sort(key=lambda x: x[0].lower())
    return folders


def print_table(rows: Iterable[Tuple[str, str]]) -> None:
    rows = list(rows)
    if not rows:
        print("No se encontraron carpetas.")
        return

    max_path = max(len(path) for path, _ in rows)
    max_path = max(max_path, len("Ruta"))

    print(f"{'Ruta'.ljust(max_path)}  ID")
    print(f"{'-' * max_path}  {'-' * 36}")
    for path, folder_id in rows:
        print(f"{path.ljust(max_path)}  {folder_id}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lista todas las carpetas de SharePoint (con su ID) para un sitio."
    )
    parser.add_argument(
        "--site-url",
        default=DEFAULT_SITE_URL,
        help=f"URL del sitio de SharePoint (por defecto: '{DEFAULT_SITE_URL}')",
    )
    parser.add_argument(
        "--site-name",
        default=None,
        help="Nombre del sitio para busqueda (fallback si no usas --site-url).",
    )
    args = parser.parse_args()

    credential = build_credential()
    token = get_token(credential)

    if args.site_url:
        site = get_site_by_url(args.site_url, token)
        source_label = f"URL: {args.site_url}"
    else:
        target_name = args.site_name or DEFAULT_SITE_NAME
        site = search_site(target_name, token)
        source_label = f"Busqueda por nombre: {target_name}"

    site_id = site["id"]
    site_name = site.get("displayName", "(sin nombre)")

    drive = get_default_drive(site_id, token)
    drive_id = drive["id"]
    drive_name = drive.get("name", "(sin nombre)")

    print(f"Origen: {source_label}")
    print(f"Sitio: {site_name}")
    print(f"Site ID: {site_id}")
    print(f"Drive: {drive_name}")
    print(f"Drive ID: {drive_id}")
    print()

    folders = list_folders(site_id, drive_id, token)
    print_table(folders)
    print()
    print(f"Total carpetas: {len(folders)}")


if __name__ == "__main__":
    main()