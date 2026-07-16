from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.procesamiento_routes import router as procesamiento_router
from backend.app.utils.paths import ensure_data_directories
from backend.app.routes.descarga_routes import router as descarga_router
from backend.app.routes.catalogo_routes import router as catalogo_router


app = FastAPI(
    title="Observatorio de Precios API",
    description="Backend para procesar archivos del Observatorio de Precios",
    version="0.1.0",
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