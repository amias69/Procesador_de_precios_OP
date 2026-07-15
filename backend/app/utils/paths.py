from pathlib import Path

from backend.app import config


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_data_directories() -> None:
    directories = [
        config.CATALOGO_ORIGINAL_DIR,
        config.CATALOGO_LIMPIO_DIR,
        config.UPLOADS_DIR,
        config.OUTPUTS_DIR,
        config.REPORTS_DIR,
    ]

    for directory in directories:
        ensure_directory(directory)


def get_upload_path(filename: str) -> Path:
    return config.UPLOADS_DIR / filename


def get_output_path(filename: str) -> Path:
    return config.OUTPUTS_DIR / filename


def get_report_path(filename: str) -> Path:
    return config.REPORTS_DIR / filename