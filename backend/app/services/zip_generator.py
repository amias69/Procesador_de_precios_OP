from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def generate_zip(
    csv_path: Path,
    zip_path: Path,
) -> Path:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo CSV: {csv_path}"
        )

    zip_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ZipFile(
        zip_path,
        mode="w",
        compression=ZIP_DEFLATED,
    ) as zip_file:
        zip_file.write(
            csv_path,
            arcname=csv_path.name,
        )

    return zip_path