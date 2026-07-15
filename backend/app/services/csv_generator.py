from pathlib import Path

import pandas as pd

from backend.app import config
from backend.app.validators.precio_validator import format_price


def build_output_dataframe(valid_records: list[dict]) -> pd.DataFrame:
    output_rows: list[dict[str, str]] = []

    for record in valid_records:
        output_rows.append(
            {
                "CodEstab": str(record["CodEstab"]),
                "CodProd": str(record["CodProd"]),
                "Precio 1": format_price(record["precio_empaque"]),
                "Precio 2": format_price(record["precio_unidad"]),
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