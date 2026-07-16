from pathlib import Path

import pandas as pd


COLUMNAS_CATALOGO = [
    "codigo_producto",
    "nombre_producto",
    "concentracion",
    "forma_farmaceutica",
    "presentacion",
    "unidades_por_envase",
    "registro_sanitario",
    "laboratorio",
    "fabricante",
    "principio_activo",
]


def limpiar_catalogo(
    archivo_entrada: str | Path,
    archivo_salida: str | Path,
) -> Path:
    """
    Limpia y normaliza el catálogo oficial descargado
    desde el Observatorio de DIGEMID.

    Parámetros:
        archivo_entrada:
            Ruta del archivo Excel original descargado.

        archivo_salida:
            Ruta donde se guardará el catálogo limpio.

    Retorna:
        Path con la ruta del catálogo limpio generado.
    """
    archivo_entrada = Path(archivo_entrada)
    archivo_salida = Path(archivo_salida)

    if not archivo_entrada.exists():
        raise FileNotFoundError(
            f"No existe el catálogo original: {archivo_entrada}"
        )

    if archivo_entrada.suffix.lower() not in {".xlsx", ".xls"}:
        raise ValueError(
            "El catálogo original debe ser un archivo Excel "
            "con extensión .xlsx o .xls."
        )

    archivo_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_excel(
        archivo_entrada,
        skiprows=6,
    )

    if df.shape[1] < len(COLUMNAS_CATALOGO):
        raise ValueError(
            f"El catálogo contiene solamente {df.shape[1]} columnas, "
            f"pero se esperaban al menos {len(COLUMNAS_CATALOGO)}."
        )

    df = df.iloc[:, :10].copy()

    df.columns = COLUMNAS_CATALOGO

    df = df.dropna(
        how="all"
    )

    for columna in df.select_dtypes(
        include="object"
    ).columns:
        df[columna] = df[columna].str.strip()

    df.to_excel(
        archivo_salida,
        index=False,
        engine="openpyxl",
    )

    return archivo_salida