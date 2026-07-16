from fastapi import APIRouter, HTTPException

from backend.app import config
from backend.app.services.catalogo_cleaner import limpiar_catalogo
from backend.app.services.catalogo_downloader import descargar_catalogo


router = APIRouter(
    prefix="/catalogo",
    tags=["Catálogo"],
)


@router.post("/actualizar")
def actualizar_catalogo():
    """
    Descarga el catálogo oficial más reciente de DIGEMID,
    lo limpia y actualiza el catálogo interno utilizado
    por la aplicación.
    """
    try:
        archivo_original = descargar_catalogo(
            archivo_salida=config.CATALOGO_ORIGINAL_PATH,
            headless=True,
        )

        archivo_limpio = limpiar_catalogo(
            archivo_entrada=archivo_original,
            archivo_salida=config.CATALOGO_LIMPIO_PATH,
        )

        return {
            "message": "Catálogo actualizado correctamente.",
            "archivo_original": archivo_original.name,
            "archivo_limpio": archivo_limpio.name,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo actualizar el catálogo: {error}",
        ) from error


@router.get("/estado")
def obtener_estado_catalogo():
    """
    Informa si el catálogo original y el catálogo limpio
    existen actualmente en el servidor.
    """
    original_existe = config.CATALOGO_ORIGINAL_PATH.exists()
    limpio_existe = config.CATALOGO_LIMPIO_PATH.exists()

    return {
        "catalogo_original": {
            "existe": original_existe,
            "archivo": config.CATALOGO_ORIGINAL_PATH.name,
        },
        "catalogo_limpio": {
            "existe": limpio_existe,
            "archivo": config.CATALOGO_LIMPIO_PATH.name,
        },
        "listo_para_procesar": limpio_existe,
    }