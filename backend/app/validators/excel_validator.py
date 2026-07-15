from pathlib import Path

import pandas as pd

from backend.app import config


def validate_excel_extension(filename: str) -> list[str]:
    errors: list[str] = []
    extension = Path(filename).suffix.lower()

    if extension not in config.ALLOWED_EXCEL_EXTENSIONS:
        allowed_extensions = ", ".join(
            sorted(config.ALLOWED_EXCEL_EXTENSIONS)
        )

        errors.append(
            f"El archivo debe tener una extensión permitida: "
            f"{allowed_extensions}."
        )

    return errors


def validate_required_columns(columns: list[str]) -> list[str]:
    errors: list[str] = []

    normalized_columns = {
        str(column).strip()
        for column in columns
    }

    missing_columns = (
        config.REQUIRED_INPUT_COLUMNS
        - normalized_columns
    )

    if missing_columns:
        missing_text = ", ".join(
            sorted(missing_columns)
        )

        errors.append(
            f"Faltan columnas obligatorias: {missing_text}."
        )

    return errors


def read_excel_headers(path: Path) -> list[str]:
    extension = path.suffix.lower()

    if extension == ".ods":
        dataframe = pd.read_excel(
            path,
            engine="odf",
            nrows=0,
        )
    else:
        dataframe = pd.read_excel(
            path,
            nrows=0,
        )

    return [
        str(column).strip()
        for column in dataframe.columns
    ]


def validate_excel_file(path: Path) -> list[str]:
    errors = validate_excel_extension(path.name)

    if errors:
        return errors

    if not path.exists():
        return ["No se encontró el archivo seleccionado."]

    if path.stat().st_size == 0:
        return ["El archivo seleccionado está vacío."]

    try:
        columns = read_excel_headers(path)
    except Exception:
        return [
            "No se pudo leer el archivo. "
            "Verifica que sea un archivo .xlsx, .xls u .ods válido "
            "y que no esté dañado."
        ]

    errors.extend(
        validate_required_columns(columns)
    )

    return errors