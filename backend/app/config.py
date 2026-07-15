from pathlib import Path


APP_NAME = "Generador Observatorio de Precios"
APP_VERSION = "0.1.0"


BASE_DIR = Path(__file__).resolve().parents[2]

BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

DATA_DIR = BACKEND_DIR / "data"
CATALOGO_ORIGINAL_DIR = DATA_DIR / "catalogo_original"
CATALOGO_LIMPIO_DIR = DATA_DIR / "catalogo_limpio"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUTS_DIR = DATA_DIR / "outputs"
REPORTS_DIR = DATA_DIR / "reports"
CATALOGO_ORIGINAL_FILENAME = "catalogoproductos.xlsx"
CATALOGO_LIMPIO_FILENAME = "catalogoproductos_limpio.xlsx"

CATALOGO_ORIGINAL_PATH = (
    CATALOGO_ORIGINAL_DIR / CATALOGO_ORIGINAL_FILENAME
)

CATALOGO_LIMPIO_PATH = (
    CATALOGO_LIMPIO_DIR / CATALOGO_LIMPIO_FILENAME
)

ALLOWED_EXCEL_EXTENSIONS = {".xlsx", ".xls", ".ods"}

REQUIRED_INPUT_COLUMNS = {
    "registro_sanitario",
    "precio_empaque",
    "precio_unidad",
}

OUTPUT_COLUMNS = [
    "CodEstab",
    "CodProd",
    "Precio 1",
    "Precio 2",
]

TIPOS_PROCESO = {
    "CARGA ARCHIVO",
    "LEVANTAROBSERVADO",
    "CARGA ARCHIVO_P1",
}