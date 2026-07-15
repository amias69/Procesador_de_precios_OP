from pathlib import Path

import pandas as pd


def generate_report(
    records: list[dict],
    output_path: Path,
    sheet_name: str,
) -> Path:
    if not records:
        raise ValueError(
            "No existen registros para generar este reporte."
        )

    if output_path.suffix.lower() != ".ods":
        raise ValueError(
            "El reporte debe generarse con extensión .ods."
        )

    dataframe = pd.DataFrame(records)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_excel(
        output_path,
        index=False,
        engine="odf",
        sheet_name=sheet_name,
    )

    return output_path