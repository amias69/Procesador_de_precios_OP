from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.app import config
from backend.app.services.csv_generator import generate_csv
from backend.app.services.processor import process_price_file
from backend.app.services.report_generator import generate_report
from backend.app.services.zip_generator import generate_zip
from backend.app.utils.filenames import (
    build_base_filename,
    build_csv_filename,
    build_report_filename,
    build_zip_filename,
)
from backend.app.utils.paths import get_output_path, get_report_path, get_upload_path
from backend.app.validators.establecimiento_validator import (
    validate_establecimiento_data,
)
from backend.app.validators.excel_validator import validate_excel_extension


router = APIRouter(prefix="/procesamiento", tags=["Procesamiento"])


def save_uploaded_file(upload_file: UploadFile, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("wb") as buffer:
        buffer.write(upload_file.file.read())

    return destination


@router.post("/procesar")
async def procesar_archivo(
    archivo: UploadFile = File(...),
    ruc: str = Form(...),
    cod_estab: str = Form(...),
    mes: str = Form(...),
    anio: str = Form(...),
    tipo_proceso: str = Form(...),
) -> dict:
    errores_establecimiento = validate_establecimiento_data(
        ruc=ruc,
        cod_estab=cod_estab,
        mes=mes,
        anio=anio,
        tipo_proceso=tipo_proceso,
    )

    errores_archivo = validate_excel_extension(archivo.filename or "")

    errores = errores_establecimiento + errores_archivo

    if errores:
        raise HTTPException(
            status_code=400,
            detail=errores,
        )

    if not config.CATALOGO_LIMPIO_PATH.exists():
        raise HTTPException(
            status_code=400,
            detail=[
                "No se encontró el catálogo limpio del observatorio. "
                "Debes actualizar o preparar el catálogo antes de procesar."
            ],
        )

    upload_path = get_upload_path(archivo.filename)
    save_uploaded_file(archivo, upload_path)

    try:
        resultado = process_price_file(
            excel_path=upload_path,
            catalog_path=config.CATALOGO_LIMPIO_PATH,
            cod_estab=cod_estab,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=[str(exc)],
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=[f"Error inesperado durante el procesamiento: {exc}"],
        ) from exc

    validos = resultado["validos"]
    descartados = resultado["descartados"]
    errores_precio = resultado["errores_precio"]

    if not validos:
        raise HTTPException(
            status_code=400,
            detail=[
                "No se encontraron registros válidos para generar el archivo final."
            ],
        )

    base_filename = build_base_filename(
        ruc=ruc,
        cod_estab=cod_estab,
        mes=mes,
        anio=anio,
        tipo_proceso=tipo_proceso,
    )

    csv_filename = build_csv_filename(
        ruc=ruc,
        cod_estab=cod_estab,
        mes=mes,
        anio=anio,
        tipo_proceso=tipo_proceso,
    )
    zip_filename = build_zip_filename(
        ruc=ruc,
        cod_estab=cod_estab,
        mes=mes,
        anio=anio,
        tipo_proceso=tipo_proceso,
    )

    csv_path = get_output_path(csv_filename)
    zip_path = get_output_path(zip_filename)

    generate_csv(valid_records=validos, output_path=csv_path)
    generate_zip(csv_path=csv_path, zip_path=zip_path)

    reportes_generados: dict[str, str] = {}

    if validos:
        validos_report_name = build_report_filename(
            "VALIDOS",
            base_filename,
        )
        validos_report_path = get_report_path(validos_report_name)

        generate_report(
            records=validos,
            output_path=validos_report_path,
            sheet_name="Validos",
        )
        reportes_generados["validos"] = validos_report_path.name

    if descartados:
        descartados_report_name = build_report_filename(
            "DESCARTADOS",
            base_filename,
        )
        descartados_report_path = get_report_path(descartados_report_name)
        descartados_report_path = get_report_path(
            descartados_report_name.replace(".csv", ".ods")
        )

        generate_report(
            records=descartados,
            output_path=descartados_report_path,
            sheet_name="Descartados",
        )
        reportes_generados["descartados"] = descartados_report_path.name

    if errores_precio:
        errores_report_name = build_report_filename(
            "ERRORES_PRECIO",
            base_filename,
        )
        errores_report_path = get_report_path(errores_report_name)

        generate_report(
            records=errores_precio,
            output_path=errores_report_path,
            sheet_name="ErroresPrecio",
        )
        reportes_generados["errores_precio"] = errores_report_path.name

    return {
        "message": "Archivo procesado correctamente.",
        "archivo_final_csv": csv_path.name,
        "archivo_final_zip": zip_path.name,
        "reportes": reportes_generados,
        "resumen": {
            "validos": len(validos),
            "descartados": len(descartados),
            "errores_precio": len(errores_precio),
        },
    }