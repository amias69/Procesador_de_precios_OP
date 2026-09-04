from pathlib import Path

import pandas as pd

from backend.app import config
from backend.app.validators.precio_validator import (format_price, parse_price,)


def build_output_dataframe(valid_records: list[dict]) -> pd.DataFrame:
    output_rows: list[dict[str, str]] = []

    for record in valid_records:
        precio_unidad = parse_price(
            record["precio_unidad"]
        )
        unidades_por_empaque = parse_price(
            record["unidades_por_empaque"]
        )

        # El precio por empaque se calcula siempre usando
        # el precio unitario y las unidades oficiales del catálogo.
        precio_empaque_final = (
            precio_unidad * unidades_por_empaque
        )

        output_rows.append(
            {
                "CodEstab": str(record["CodEstab"]),
                "CodProd": str(record["CodProd"]),
                "Precio 1": format_price(precio_empaque_final),
                "Precio 2": format_price(precio_unidad),
            }
        )

    return pd.DataFrame(
        output_rows,
        columns=config.OUTPUT_COLUMNS,
    )


def generate_csv(
    valid_records: list[dict],
    output_path: Path,
) -> Path:
    if not valid_records:
        raise ValueError(
            "No existen registros válidos para generar el archivo CSV."
        )

    dataframe = build_output_dataframe(valid_records)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
        sep=",",
        lineterminator="\n",
    )

    return output_path