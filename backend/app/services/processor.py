from pathlib import Path

import pandas as pd

from backend.app.services.excel_reader import read_and_normalize_excel
from backend.app.validators.excel_validator import validate_excel_file
from backend.app.validators.precio_validator import validate_price
from backend.app.utils.value_normalizers import normalize_excel_text


def load_catalog_dataframe(catalog_path: Path) -> pd.DataFrame:
    catalog_df = pd.read_excel(catalog_path)
    catalog_df.columns = [
        str(column).strip()
        for column in catalog_df.columns
    ]

    return catalog_df


def build_catalog_lookup(
    catalog_df: pd.DataFrame,
) -> dict[str, dict]:
    required_columns = {
        "registro_sanitario",
        "codigo_producto",
        "nombre_producto",
        "unidades_por_envase",
    }

    missing_columns = required_columns - set(catalog_df.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))

        raise ValueError(
            "El catálogo limpio no contiene las columnas "
            f"requeridas: {missing_text}."
        )

    lookup: dict[str, dict] = {}

    for _, row in catalog_df.iterrows():
        registro = normalize_excel_text(
            row["registro_sanitario"]
        )

        codigo_producto = normalize_excel_text(
            row["codigo_producto"]
        )

        nombre_producto = normalize_excel_text(
            row["nombre_producto"]
        )

        unidades_por_empaque = row["Fracción"]

        if not registro or not codigo_producto:
            continue

        lookup[registro] = {
            "codigo_producto": codigo_producto,
            "nombre_producto": nombre_producto,
            "unidades_por_empaque": unidades_por_empaque,
        }

    return lookup

def process_price_file(
    excel_path: Path,
    catalog_path: Path,
    cod_estab: str,
) -> dict[str, list[dict]]:
    excel_errors = validate_excel_file(excel_path)
    if excel_errors:
        raise ValueError(" | ".join(excel_errors))

    farmacia_df = read_and_normalize_excel(excel_path)
    catalog_df = load_catalog_dataframe(catalog_path)
    catalog_lookup = build_catalog_lookup(catalog_df)

    validos: list[dict] = []
    descartados: list[dict] = []
    errores_precio: list[dict] = []

    for _, row in farmacia_df.iterrows():
        registro = normalize_excel_text(row.get("registro_sanitario", ""))
        nombre_farmacia = normalize_excel_text(
            row.get("nombre", "")
        )
        precio_empaque = row.get("precio_empaque")
        precio_unidad = row.get("precio_unidad")

        if not registro:
            descartados.append(
                {
                    "registro_sanitario": "",
                    "Nombre": nombre_farmacia,
                    "precio_empaque": precio_empaque,
                    "precio_unidad": precio_unidad,
                    "motivo": "Registro sanitario vacío.",
                }
            )
            continue

        producto_catalogo = catalog_lookup.get(registro)

        if not producto_catalogo:
            descartados.append(
                {
                    "registro_sanitario": registro,
                    "Nombre": nombre_farmacia,
                    "precio_empaque": precio_empaque,
                    "precio_unidad": precio_unidad,
                    "motivo": (
                        "Registro sanitario no encontrado "
                        "en el catálogo oficial vigente."
                    ),
                }
            )
            continue

        cod_prod = producto_catalogo["codigo_producto"]
        nombre_producto = producto_catalogo["nombre_producto"]
        unidades_por_empaque = producto_catalogo["unidades_por_empaque"]

        errores_empaque = validate_price(
            precio_empaque,
            "precio_empaque",
            allow_zero=True,
        )

        errores_unidad = validate_price(
            precio_unidad,
            "precio_unidad",
        )
        errores = errores_empaque + errores_unidad

        if errores:
            errores_precio.append(
                {
                    "registro_sanitario": registro,
                    "nombre_producto": nombre_producto,
                    "precio_empaque": precio_empaque,
                    "precio_unidad": precio_unidad,
                    "CodProd": cod_prod,
                    "CodEstab": cod_estab,
                    "motivo": " | ".join(errores),
                }
            )
            continue

        validos.append(
        {
            "registro_sanitario": registro,
            "nombre_producto": nombre_producto,
            "precio_empaque": precio_empaque,
            "precio_unidad": precio_unidad,
            "unidades_por_empaque": unidades_por_empaque,
            "CodProd": cod_prod,
            "CodEstab": cod_estab,
        }
    )

    return {
        "validos": validos,
        "descartados": descartados,
        "errores_precio": errores_precio,
    }