from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
)
from fastapi.responses import FileResponse
from backend.app import config
from backend.app.services.session_manager import (
    obtener_o_crear_session_id,
    obtener_rutas_sesion,
)

router = APIRouter(prefix="/descargas", tags=["Descargas"])


def get_safe_file_path(
    base_directory: Path,
    filename: str,
) -> Path:
    base_directory = base_directory.resolve()
    file_path = (base_directory / filename).resolve()

    if file_path.parent != base_directory:
        raise HTTPException(
            status_code=400,
            detail="Nombre de archivo inválido.",
        )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="El archivo solicitado no existe.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="La ruta solicitada no corresponde a un archivo.",
        )

    return file_path


@router.get("/archivo/{filename}")
def descargar_archivo_final(
    filename: str,
    request: Request,
    response: Response,
) -> FileResponse:
    session_id = obtener_o_crear_session_id(
        request,
        response,
    )

    session_paths = obtener_rutas_sesion(
        session_id
    )

    file_path = get_safe_file_path(
        session_paths.outputs,
        filename,
    )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )


@router.get("/reporte/{filename}")
def descargar_reporte(
    filename: str,
    request: Request,
    response: Response,
) -> FileResponse:
    session_id = obtener_o_crear_session_id(
        request,
        response,
    )

    session_paths = obtener_rutas_sesion(
        session_id
    )

    file_path = get_safe_file_path(
        session_paths.reports,
        filename,
    )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/vnd.oasis.opendocument.spreadsheet",
    )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/vnd.oasis.opendocument.spreadsheet",
    )