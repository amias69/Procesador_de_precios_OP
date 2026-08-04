from pathlib import Path

import pandas as pd


def read_excel_file(path: Path) -> pd.DataFrame:
    extension = path.suffix.lower()

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