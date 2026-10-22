from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.app import config
from backend.app.services.catalogo_cleaner import limpiar_catalogo
from backend.app.services.catalogo_downloader import descargar_catalogo
from pathlib import Path
from datetime import datetime

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

@router.post("/cargar-manual")
async def cargar_catalogo_manual(
    archivo: UploadFile = File(...),
):
    """
    Recibe manualmente el catálogo oficial de DIGEMID,
    lo guarda como catálogo original y genera
    el catálogo limpio utilizado por la aplicación.
    """
    try:
        extension = (
            Path(archivo.filename or "")
            .suffix
            .lower()
        )

        if extension not in {".xlsx", ".xls"}:
            raise HTTPException(
                status_code=400,
                detail=(
                    "El catálogo debe ser un archivo "
                    "Excel con extensión .xlsx o .xls."
                ),
            )

        config.CATALOGO_ORIGINAL_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        contenido = await archivo.read()

        config.CATALOGO_ORIGINAL_PATH.write_bytes(
            contenido
        )

        archivo_limpio = limpiar_catalogo(
            archivo_entrada=config.CATALOGO_ORIGINAL_PATH,
            archivo_salida=config.CATALOGO_LIMPIO_PATH,
        )

        return {
            "message": (
                "Catálogo cargado y procesado "
                "correctamente."
            ),
            "archivo_original":
                config.CATALOGO_ORIGINAL_PATH.name,
            "archivo_limpio":
                archivo_limpio.name,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se pudo procesar el catálogo "
                f"cargado manualmente: {error}"
            ),
        ) from error
        
def obtener_ultima_actualizacion_catalogo():
    if not config.CATALOGO_LIMPIO_PATH.exists():
        return None

    timestamp = config.CATALOGO_LIMPIO_PATH.stat().st_mtime

    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

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
        "ultima_actualizacion": obtener_ultima_actualizacion_catalogo(),
    }