import asyncio
import html
import importlib
import os
import queue
import sys
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict

import streamlit as st
from dotenv import dotenv_values, set_key

ENV_FILE = Path(__file__).with_name(".env")
WORKER_FINISHED = "__WORKER_FINISHED__"
ENV_KEYS = [
    "TENANT_ID",
    "CLIENT_ID_DELEGATED",
    "CLIENT_ID_APPONLY",
    "CLIENT_SECRET",
    "DRIVE_ID",
    "SITE_ID",
    "SHAREPOINT_FOLDER_ID",
]


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _load_env_values() -> Dict[str, str]:
    values = dotenv_values(ENV_FILE) if ENV_FILE.exists() else {}
    return {key: str(values.get(key, "") or os.getenv(key, "") or "") for key in ENV_KEYS}


def _save_env(values: Dict[str, str]) -> None:
    ENV_FILE.touch(exist_ok=True)
    for key, value in values.items():
        set_key(str(ENV_FILE), key, value)
        os.environ[key] = value


def _worker(stop_event: threading.Event, log_queue: "queue.Queue[str]", poll_seconds: int, env_values: Dict[str, str]):
    def log(message: str):
        log_queue.put(f"[{_now()}] {message}")

    for key, value in env_values.items():
        os.environ[key] = value

    try:
        _ensure_venv_site_packages()
        import leer_emails_nuevos as email_worker

        email_worker = importlib.reload(email_worker)
        log("Worker iniciado.")

        async def _run():
            await email_worker.me(log_fn=log)
            await email_worker.leer_correos(
                stop_event=stop_event,
                poll_seconds=poll_seconds,
                log_fn=log,
            )

        asyncio.run(_run())
    except Exception:
        log("ERROR no controlado en worker:")
        for line in traceback.format_exc().splitlines():
            log(line)
    finally:
        log("Worker detenido.")
        log_queue.put(WORKER_FINISHED)


def _ensure_venv_site_packages():
    current = Path(__file__).resolve()
    candidates = [
        current.parent / "venv" / "Lib" / "site-packages",
        current.parent.parent / "venv" / "Lib" / "site-packages",
    ]
    for site_packages in candidates:
        if site_packages.exists():
            path_str = str(site_packages)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)


def _init_state():
    if "running" not in st.session_state:
        st.session_state.running = False
    if "worker_thread" not in st.session_state:
        st.session_state.worker_thread = None
    if "stop_event" not in st.session_state:
        st.session_state.stop_event = None
    if "log_queue" not in st.session_state:
        st.session_state.log_queue = queue.Queue()
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "env_values" not in st.session_state:
        st.session_state.env_values = _load_env_values()


def _drain_logs():
    while True:
        try:
            entry = st.session_state.log_queue.get_nowait()
        except queue.Empty:
            break

        if entry == WORKER_FINISHED:
            st.session_state.running = False
            st.session_state.worker_thread = None
            st.session_state.stop_event = None
        else:
            st.session_state.logs.append(entry)

    st.session_state.logs = st.session_state.logs[-1000:]


def _cargar_carpetas_sharepoint(site_url: str):
    _ensure_venv_site_packages()
    import listar_carpetas_sharepoint as lcs

    credential = lcs.build_credential()
    token = lcs.get_token(credential)
    site = lcs.get_site_by_url(site_url, token)
    site_id = site["id"]
    drive = lcs.get_default_drive(site_id, token)
    drive_id = drive["id"]
    folders = lcs.list_folders(site_id, drive_id, token)
    return folders


def main():
    st.set_page_config(page_title="Procesador de Emails", layout="wide")
    _ensure_venv_site_packages()
    st.title("Procesador de Emails a SharePoint")
    _init_state()
    _drain_logs()

    top1, top2, top3 = st.columns([1, 1, 2])
    with top1:
        start_clicked = st.button("Arrancar", type="primary", use_container_width=True, disabled=st.session_state.running)
    with top2:
        stop_clicked = st.button("Parar", use_container_width=True, disabled=not st.session_state.running)
    with top3:
        poll_seconds = st.number_input("Intervalo de lectura (segundos)", min_value=1, max_value=300, value=5, step=1)

    if start_clicked and not st.session_state.running:
        _save_env(st.session_state.env_values)
        stop_event = threading.Event()
        worker_thread = threading.Thread(
            target=_worker,
            args=(stop_event, st.session_state.log_queue, int(poll_seconds), dict(st.session_state.env_values)),
            daemon=True,
        )
        st.session_state.stop_event = stop_event
        st.session_state.worker_thread = worker_thread
        st.session_state.running = True
        st.session_state.logs.append(f"[{_now()}] Arranque solicitado.")
        worker_thread.start()

    if stop_clicked and st.session_state.running and st.session_state.stop_event is not None:
        st.session_state.stop_event.set()
        st.session_state.logs.append(f"[{_now()}] Parada solicitada.")

    status = "En ejecucion" if st.session_state.running else "Detenido"
    st.write(f"Estado: {status}")

    left_col, right_col = st.columns([1, 1.3], vertical_alignment="top")
    with left_col:
        with st.form("env_form", clear_on_submit=False):
            st.subheader("Variables de Entorno")
            for key in ENV_KEYS:
                st.session_state.env_values[key] = st.text_input(
                    key,
                    value=st.session_state.env_values.get(key, ""),
                    type="password" if key == "CLIENT_SECRET" else "default",
                )
            save_clicked = st.form_submit_button("Guardar .env")

        if save_clicked:
            _save_env(st.session_state.env_values)
            st.success(f"Configuracion guardada en {ENV_FILE}")

    with right_col:
        st.subheader("Actividad")
        reverse_logs = list(reversed(st.session_state.logs))
        log_html = html.escape("\n".join(reverse_logs))
        st.markdown(
            f"""
<div id="logbox" style="height:520px;overflow-y:auto;border:1px solid #ddd;padding:8px;background:#111;color:#eee;font-family:Consolas, monospace;font-size:12px;white-space:pre-wrap;">
{log_html}
</div>
<script>
const box = window.parent.document.getElementById("logbox");
if (box) {{
  box.scrollTop = 0;
}}
</script>
""",
            unsafe_allow_html=True,
        )

    st.subheader("Carpetas SharePoint")
    folder_site_url = st.text_input(
        "URL del sitio para listar carpetas",
        value=st.session_state.env_values.get("SHAREPOINT_SITE_URL", "https://cursograph.sharepoint.com/sites/GRUPOFUERTES-ELPOZOCURSO"),
        key="folders_site_url",
    )
    refresh_folders = st.button("Actualizar carpetas", use_container_width=False)
    if "folders_cache" not in st.session_state:
        st.session_state.folders_cache = []
    if "folders_error" not in st.session_state:
        st.session_state.folders_error = ""

    if refresh_folders:
        try:
            st.session_state.folders_cache = _cargar_carpetas_sharepoint(folder_site_url)
            st.session_state.folders_error = ""
        except Exception as e:
            st.session_state.folders_error = str(e)

    if st.session_state.folders_error:
        st.error(st.session_state.folders_error)

    if st.session_state.folders_cache:
        rows = [{"Ruta": path, "ID": folder_id} for path, folder_id in st.session_state.folders_cache]
        st.dataframe(rows, use_container_width=True, height=260)
    else:
        st.info("Pulsa 'Actualizar carpetas' para cargar la lista.")

    if st.session_state.running:
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()
