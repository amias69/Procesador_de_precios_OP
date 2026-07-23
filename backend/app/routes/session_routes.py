from fastapi import APIRouter, Request, Response

from backend.app.services.session_manager import (
    obtener_rutas_sesion,
    obtener_o_crear_session_id,
)


router = APIRouter(
    prefix="/session",
    tags=["session"],
)


@router.get("/estado")
def obtener_estado_sesion(
    request: Request,
    response: Response,
):
    session_id = obtener_o_crear_session_id(
        request,
        response,
    )

    obtener_rutas_sesion(
        session_id
    )

    return {
        "session_id": session_id,
    }