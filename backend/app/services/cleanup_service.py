from pathlib import Path
import shutil


def vaciar_directorio(directorio: Path) -> None:
    """
    Elimina todo el contenido de un directorio,
    pero conserva el directorio principal.
    """
    directorio.mkdir(
        parents=True,
        exist_ok=True,
    )

    for elemento in directorio.iterdir():
        if elemento.is_dir():
            shutil.rmtree(elemento)
        else:
            elemento.unlink()


def limpiar_temporales(
    directorios: list[Path],
) -> None:
    """
    Limpia todas las carpetas temporales
    utilizadas por la aplicación.
    """
    for directorio in directorios:
        vaciar_directorio(
            directorio
        )