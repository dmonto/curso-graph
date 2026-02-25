import argparse
import asyncio
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
DEFAULT_SITE_URL = "https://cursograph.sharepoint.com/sites/GRUPOFUERTES-ELPOZOCURSO"
DEFAULT_TARGET_FOLDER_ID = "01NT23UIUPOKO3FCNXHFHZPL322E4G372F"

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID_APPONLY = os.getenv("CLIENT_ID_APPONLY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENV_DRIVE_ID = os.getenv("DRIVE_ID")
ENV_SITE_ID = os.getenv("SITE_ID")

if not TENANT_ID or not CLIENT_ID_APPONLY or not CLIENT_SECRET:
    raise RuntimeError(
        "Faltan TENANT_ID, CLIENT_ID_APPONLY o CLIENT_SECRET en .env para autenticacion app-only."
    )

credential_apponly = ClientSecretCredential(
    client_id=CLIENT_ID_APPONLY,
    tenant_id=TENANT_ID,
    client_secret=CLIENT_SECRET,
)


def _safe_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "_", filename).strip() or "archivo.bin"


def _get_access_token() -> str:
    return credential_apponly.get_token("https://graph.microsoft.com/.default").token


def _graph_get(url: str, token: str, params: Optional[Dict[str, str]] = None) -> Dict:
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Graph GET {url} -> {response.status_code}: {response.text}")
    return response.json()


def _graph_get_optional(url: str, token: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict]:
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    if response.status_code == 404:
        return None
    if response.status_code >= 400:
        raise RuntimeError(f"Graph GET {url} -> {response.status_code}: {response.text}")
    return response.json()


def _get_site_id_from_url(site_url: str, token: str) -> str:
    parsed = urlparse(site_url)
    if not parsed.netloc or not parsed.path:
        raise RuntimeError(f"URL de sitio no valida: {site_url}")

    endpoint = f"{GRAPH_BASE}/sites/{parsed.netloc}:{parsed.path.rstrip('/')}"
    data = _graph_get(endpoint, token)
    site_id = data.get("id")
    if not site_id:
        raise RuntimeError(f"No se pudo resolver site_id para: {site_url}")
    return site_id


def _list_site_drives(site_id: str, token: str) -> List[Dict]:
    drives: List[Dict] = []
    next_url = f"{GRAPH_BASE}/sites/{site_id}/drives"
    params: Optional[Dict[str, str]] = {"$select": "id,name,webUrl,driveType"}

    while next_url:
        data = _graph_get(next_url, token, params=params)
        params = None
        drives.extend(data.get("value", []))
        next_url = data.get("@odata.nextLink")

    return drives


def _find_folder_drive(
    folder_id: str,
    token: str,
    site_id: Optional[str],
    preferred_drive_id: Optional[str],
) -> Tuple[str, Dict]:
    candidate_drive_ids: List[str] = []

    if preferred_drive_id:
        candidate_drive_ids.append(preferred_drive_id)

    if site_id:
        for drive in _list_site_drives(site_id, token):
            drive_id = drive.get("id")
            if drive_id and drive_id not in candidate_drive_ids:
                candidate_drive_ids.append(drive_id)

    if not candidate_drive_ids:
        raise RuntimeError(
            "No hay drive_id candidatos para buscar la carpeta. Define DRIVE_ID o SITE_ID/site-url."
        )

    for drive_id in candidate_drive_ids:
        item = _graph_get_optional(
            f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_id}",
            token,
            params={"$select": "id,name,parentReference,webUrl"},
        )
        if item is not None:
            return drive_id, item

    raise RuntimeError(
        "No se encontro el folder_id en los drives probados. "
        f"folder_id={folder_id}, drives={candidate_drive_ids}"
    )


def _upload_to_folder(drive_id: str, folder_id: str, filename: str, content: bytes, token: str) -> None:
    url = f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_id}:/{filename}:/content"
    response = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
        },
        data=content,
        timeout=120,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Graph PUT {url} -> {response.status_code}: {response.text}")


async def subir_fichero(local_file: Path, folder_id: str, drive_id: str, token: str) -> None:
    content = local_file.read_bytes()
    safe_name = _safe_filename(local_file.name)
    await asyncio.to_thread(_upload_to_folder, drive_id, folder_id, safe_name, content, token)
    print(f"OK: {local_file.name}")


async def subir_desde_carpeta(
    source_dir: Path,
    folder_id: str,
    recursive: bool,
    site_url: Optional[str],
    drive_id_arg: Optional[str],
) -> None:
    if not source_dir.exists() or not source_dir.is_dir():
        raise RuntimeError(f"La ruta de origen no existe o no es carpeta: {source_dir}")

    token = _get_access_token()

    site_id: Optional[str] = None
    if site_url:
        site_id = _get_site_id_from_url(site_url, token)
    elif ENV_SITE_ID:
        site_id = ENV_SITE_ID

    preferred_drive_id = drive_id_arg or ENV_DRIVE_ID
    drive_id, folder_item = _find_folder_drive(folder_id, token, site_id, preferred_drive_id)

    files = sorted(source_dir.rglob("*") if recursive else source_dir.glob("*"))
    files = [f for f in files if f.is_file()]

    if not files:
        print(f"No hay archivos para subir en: {source_dir}")
        return

    print(f"Site ID: {site_id or '(no definido)'}")
    print(f"Drive ID resuelto: {drive_id}")
    print(f"Folder destino: {folder_item.get('name', '(sin nombre)')} ({folder_id})")
    print(f"Subiendo {len(files)} archivo(s) desde: {source_dir}")

    for file_path in files:
        await subir_fichero(file_path, folder_id, drive_id, token)


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sube ficheros de una carpeta local a una carpeta de SharePoint por folder_id."
    )
    parser.add_argument(
        "--source",
        default="adjuntos",
        help="Carpeta local con archivos a subir (por defecto: adjuntos)",
    )
    parser.add_argument(
        "--folder-id",
        default=DEFAULT_TARGET_FOLDER_ID,
        help=f"ID de carpeta destino en SharePoint (por defecto: {DEFAULT_TARGET_FOLDER_ID})",
    )
    parser.add_argument(
        "--site-url",
        default=DEFAULT_SITE_URL,
        help=f"URL del sitio SharePoint (por defecto: {DEFAULT_SITE_URL})",
    )
    parser.add_argument(
        "--drive-id",
        default=None,
        help="Drive ID preferido (opcional). Si no coincide con el folder, se buscara en los drives del sitio.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Incluye subcarpetas de la ruta de origen.",
    )

    args = parser.parse_args()
    source_dir = Path(args.source)

    await subir_desde_carpeta(
        source_dir=source_dir,
        folder_id=args.folder_id,
        recursive=args.recursive,
        site_url=args.site_url,
        drive_id_arg=args.drive_id,
    )


if __name__ == "__main__":
    asyncio.run(main())