from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4
import shutil
from datetime import datetime, timedelta
from fastapi import Request, Response
from backend.app import config


SESSION_COOKIE_NAME = "session_id"
SESSION_TTL_HOURS = 24  # Tiempo de vida de la sesión en horas

@dataclass
class SessionPaths:
    root: Path
    uploads: Path
    outputs: Path
    reports: Path


def crear_session_id() -> str:
    return uuid4().hex


def obtener_o_crear_session_id(
    request: Request,
    response: Response,
) -> str: 
    limpiar_sesiones_expiradas() 
    session_id = request.cookies.get(
        SESSION_COOKIE_NAME
    )

    if not session_id:
        session_id = crear_session_id()

        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            samesite="lax",
        )

    actualizar_actividad_sesion(
        session_id
    )

    return session_id

def limpiar_sesiones_expiradas() -> None:
    if not config.SESSIONS_DIR.exists():
        return

    limite = datetime.now() - timedelta(
        hours=SESSION_TTL_HOURS
    )

    for session_dir in config.SESSIONS_DIR.iterdir():
        if not session_dir.is_dir():
            continue

        marcador = (
            session_dir
            / ".last_activity"
        )

        if not marcador.exists():
            continue

        ultima_actividad = datetime.fromtimestamp(
            marcador.stat().st_mtime
        )

        if ultima_actividad < limite:
            shutil.rmtree(
                session_dir,
                ignore_errors=True,
            )

def obtener_rutas_sesion(
    session_id: str,
) -> SessionPaths:
    root = config.SESSIONS_DIR / session_id

    uploads = root / "uploads"
    outputs = root / "outputs"
    reports = root / "reports"

    for directorio in (
        uploads,
        outputs,
        reports,
    ):
        directorio.mkdir(
            parents=True,
            exist_ok=True,
        )

    return SessionPaths(
        root=root,
        uploads=uploads,
        outputs=outputs,
        reports=reports,
    )

def actualizar_actividad_sesion(
    session_id: str,
) -> None:
    session_dir = (
        config.SESSIONS_DIR
        / session_id
    )

    session_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    marcador = (
        session_dir
        / ".last_activity"
    )

    marcador.touch()