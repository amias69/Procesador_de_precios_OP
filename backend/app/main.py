from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.procesamiento_routes import router as procesamiento_router
from backend.app.utils.paths import ensure_data_directories
from backend.app.routes.descarga_routes import router as descarga_router
from backend.app.routes.catalogo_routes import router as catalogo_router

from contextlib import asynccontextmanager

from backend.app import config
from backend.app.services.cleanup_service import limpiar_temporales

@asynccontextmanager
async def lifespan(app: FastAPI):
    directorios_temporales = [
        config.UPLOADS_DIR,
        config.OUTPUTS_DIR,
        config.REPORTS_DIR,
        config.CATALOGO_ORIGINAL_DIR,
        config.CATALOGO_LIMPIO_DIR,
    ]

    # Limpieza preventiva al iniciar
    limpiar_temporales(
        directorios_temporales
    )

    yield

    # Limpieza al cerrar normalmente
    limpiar_temporales(
        directorios_temporales
    )
    
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    lifespan=lifespan,
)

ensure_data_directories()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(procesamiento_router)
app.include_router(descarga_router)
app.include_router(catalogo_router)


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"message": "Backend del Observatorio de Precios en funcionamiento"}