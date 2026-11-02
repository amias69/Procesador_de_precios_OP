import csv
from pathlib import Path

import pandas as pd


def read_csv_file(path: Path) -> pd.DataFrame:
    """Lee un CSV detectando el separador y codificaciones habituales."""
    # UTF-8 con o sin BOM, Windows-1252 y Latin-1 cubren exportaciones comunes.
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open("r", encoding=encoding, newline="") as file:
                sample = file.read(8192)

            # Restringimos la detección a delimitadores habituales de CSV.
            try:
                delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
            except csv.Error:
                delimiter = ","

            return pd.read_csv(path, sep=delimiter, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeError(f"No se pudo decodificar el archivo CSV: {path}")


def read_excel_file(path: Path) -> pd.DataFrame:
    """Lee hojas de cálculo y CSV conservando la interfaz existente."""
    extension = path.suffix.lower()

    if extension == ".csv":
        return read_csv_file(path)

    if extension == ".ods":
        return pd.read_excel(path, engine="odf")

    return pd.read_excel(path)


def normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()
    dataframe.columns = [
        str(column).strip().lower()
        for column in dataframe.columns
    ]
    return dataframe


def read_and_normalize_excel(path: Path) -> pd.DataFrame:
    dataframe = read_excel_file(path)
    return normalize_columns(dataframe)
