import asyncio
import base64
import json
import os
import re
import requests
from typing import Callable, Optional

from azure.identity import InteractiveBrowserCredential
from dotenv import load_dotenv
from msgraph import GraphServiceClient
from msgraph.generated.models.message import Message

import subir_ficheros_sharepoint as sp_upload

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID_DELEGATED") or input("Client ID:")
TENANT_ID = os.getenv("TENANT_ID")

credential = InteractiveBrowserCredential(client_id=CLIENT_ID, tenant_id=TENANT_ID)
scopes = [
    "User.Read",
    "Mail.Read",
    "Mail.ReadWrite",
]
client = GraphServiceClient(credentials=credential, scopes=scopes)

TARGET_SHAREPOINT_FOLDER_ID = (
    os.getenv("SHAREPOINT_FOLDER_ID")
    or os.getenv("TARGET_SHAREPOINT_FOLDER_ID")
    or sp_upload.DEFAULT_TARGET_FOLDER_ID
)
TARGET_SITE_URL = os.getenv("SHAREPOINT_SITE_URL") or sp_upload.DEFAULT_SITE_URL
TARGET_DRIVE_ID = os.getenv("SHAREPOINT_DRIVE_ID")

_UPLOAD_CONTEXT = None
_PROCESADOS_FOLDER_ID = None
SUBJECT_JSON_PATTERN = re.compile(r"^\s*([^#]+)\s*#\s*([^#]+)\s*#\s*(.+?)\s*$")


def _emit(log_fn: Optional[Callable[[str], None]], message: str):
    (log_fn or print)(message)


async def me(log_fn: Optional[Callable[[str], None]] = None):
    user = await client.me.get()
    if user:
        _emit(log_fn, user.display_name)


async def _get_upload_context(log_fn: Optional[Callable[[str], None]] = None):
    global _UPLOAD_CONTEXT
    if _UPLOAD_CONTEXT is not None:
        return _UPLOAD_CONTEXT

    token = sp_upload._get_access_token()

    site_id = None
    if TARGET_SITE_URL:
        site_id = sp_upload._get_site_id_from_url(TARGET_SITE_URL, token)
    elif sp_upload.ENV_SITE_ID:
        site_id = sp_upload.ENV_SITE_ID

    preferred_drive_id = TARGET_DRIVE_ID or sp_upload.ENV_DRIVE_ID
    drive_id, folder_item = sp_upload._find_folder_drive(
        TARGET_SHAREPOINT_FOLDER_ID,
        token,
        site_id,
        preferred_drive_id,
    )

    _UPLOAD_CONTEXT = {
        "token": token,
        "drive_id": drive_id,
        "folder_id": TARGET_SHAREPOINT_FOLDER_ID,
    }

    _emit(
        log_fn,
        "Contexto subida SharePoint: "
        f"drive={drive_id}, carpeta={folder_item.get('name', '(sin nombre)')} ({TARGET_SHAREPOINT_FOLDER_ID})"
    )
    return _UPLOAD_CONTEXT


async def subir_archivo_a_sharepoint(
    filename: str,
    content: bytes,
    log_fn: Optional[Callable[[str], None]] = None,
):
    safe_name = sp_upload._safe_filename(filename)

    last_error = None
    for attempt in range(2):
        try:
            ctx = await _get_upload_context(log_fn=log_fn)
            await asyncio.to_thread(
                sp_upload._upload_to_folder,
                ctx["drive_id"],
                ctx["folder_id"],
                safe_name,
                content,
                ctx["token"],
            )
            return
        except Exception as e:
            last_error = e
            # Si el token expiro, reconstruye contexto y reintenta una vez.
            if attempt == 0 and "401" in str(e):
                global _UPLOAD_CONTEXT
                _UPLOAD_CONTEXT = None
                continue
            break

    raise RuntimeError(f"Error subiendo '{filename}' a SharePoint: {last_error}") from last_error


async def marcar_como_leido(message_id: str):
    body = Message()
    body.is_read = True
    try:
        await client.me.messages.by_message_id(message_id).patch(body)
    except Exception as e:
        raise RuntimeError(f"No se pudo marcar como leido el mensaje {message_id}: {e}") from e


def _mail_access_token() -> str:
    return credential.get_token("https://graph.microsoft.com/Mail.ReadWrite").token


def _graph_get_sync(url: str, token: str, params=None):
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Graph GET {url} -> {response.status_code}: {response.text}")
    return response.json()


def _graph_post_sync(url: str, token: str, payload=None):
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Graph POST {url} -> {response.status_code}: {response.text}")
    if response.text:
        return response.json()
    return {}


async def _asegurar_carpeta_procesados() -> str:
    global _PROCESADOS_FOLDER_ID
    if _PROCESADOS_FOLDER_ID:
        return _PROCESADOS_FOLDER_ID

    token = _mail_access_token()
    list_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
    data = await asyncio.to_thread(
        _graph_get_sync,
        list_url,
        token,
        {
            "$filter": "displayName eq 'procesados'",
            "$select": "id,displayName",
            "$top": "1",
        },
    )

    existing = (data.get("value") or [])
    if existing:
        _PROCESADOS_FOLDER_ID = existing[0]["id"]
        return _PROCESADOS_FOLDER_ID

    created = await asyncio.to_thread(
        _graph_post_sync,
        list_url,
        token,
        {"displayName": "procesados"},
    )
    _PROCESADOS_FOLDER_ID = created["id"]
    return _PROCESADOS_FOLDER_ID


async def mover_correo_a_procesados(message_id: str):
    folder_id = await _asegurar_carpeta_procesados()
    token = _mail_access_token()
    move_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/move"
    await asyncio.to_thread(
        _graph_post_sync,
        move_url,
        token,
        {"destinationId": folder_id},
    )


async def mover_adjuntos_a_sharepoint(
    message_id: str,
    log_fn: Optional[Callable[[str], None]] = None,
):
    attachments = await client.me.messages.by_message_id(message_id).attachments.get()
    if not attachments or not attachments.value:
        return 0

    moved = 0
    for attachment in attachments.value:
        if getattr(attachment, "odata_type", "") != "#microsoft.graph.fileAttachment":
            continue
        if not getattr(attachment, "content_bytes", None):
            continue

        raw = attachment.content_bytes
        content = base64.b64decode(raw) if isinstance(raw, str) else raw
        filename = getattr(attachment, "name", None) or "adjunto.bin"

        await subir_archivo_a_sharepoint(filename, content, log_fn=log_fn)
        moved += 1

    return moved


def _payload_desde_asunto(subject: str):
    match = SUBJECT_JSON_PATTERN.match(subject or "")
    if not match:
        return None

    objeto, campo, dato = (part.strip() for part in match.groups())
    if not objeto or not campo:
        return None
    return {objeto: {campo: dato}}


def _safe_component(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_") or "dato"


async def leer_correos(
    stop_event=None,
    poll_seconds: int = 5,
    log_fn: Optional[Callable[[str], None]] = None,
):
    while True:
        if stop_event is not None and stop_event.is_set():
            _emit(log_fn, "Parada solicitada. Fin del bucle de lectura.")
            break

        messages_page = await client.me.messages.get(
            request_configuration=client.me.messages.MessagesRequestBuilderGetRequestConfiguration(
                query_parameters=client.me.messages.MessagesRequestBuilderGetQueryParameters(
                    filter="isRead eq false",
                    top=10,
                    select=["id", "subject", "from", "receivedDateTime", "hasAttachments"],
                )
            )
        )

        _emit(log_fn, f"{'De':<30} {'Asunto':<50} {'Fecha':<25} {'Adjuntos':<10}")
        _emit(log_fn, "-" * 120)

        for message in messages_page.value:
            from_address = message.from_.email_address.address if message.from_ else "Desconocido"
            subject = message.subject if message.subject else "(Sin asunto)"
            received_date = (
                message.received_date_time.strftime("%Y-%m-%d %H:%M:%S")
                if message.received_date_time
                else "Desconocida"
            )
            has_attachments = "Si" if message.has_attachments else "No"
            _emit(log_fn, f"{from_address:<30} {subject:<50} {received_date:<25} {has_attachments:<10}")

            processed = False

            if message.has_attachments and message.id:
                moved = await mover_adjuntos_a_sharepoint(message.id, log_fn=log_fn)
                if moved:
                    processed = True
                    _emit(log_fn, f"  -> {moved} adjunto(s) movido(s) a SharePoint.")
            elif not message.has_attachments and message.id:
                payload = _payload_desde_asunto(message.subject or "")
                if payload is not None:
                    objeto = next(iter(payload.keys()))
                    filename = f"{_safe_component(objeto)}_{message.id}.json"
                    content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                    await subir_archivo_a_sharepoint(filename, content, log_fn=log_fn)
                    processed = True
                    _emit(log_fn, f"  -> JSON creado desde asunto y subido: {filename}")

            if processed and message.id:
                await marcar_como_leido(message.id)
                await mover_correo_a_procesados(message.id)
                _emit(log_fn, "  -> Correo movido a carpeta 'procesados'.")

        _emit(log_fn, f"\nEsperando {poll_seconds} segundos...\n")
        await asyncio.sleep(poll_seconds)


async def main():
    await me()
    await leer_correos()


if __name__ == "__main__":
    asyncio.run(main())
