import math


def normalize_excel_text(value) -> str:
    """
    Convierte un valor leído desde Excel a texto limpio.

    Reglas:
    - None o NaN -> ""
    - strings -> strip()
    - floats enteros como 123.0 -> "123"
    - otros valores -> string sin espacios laterales
    """
    if value is None:
        return ""

    if isinstance(value, float):
        if math.isnan(value):
            return ""

        if value.is_integer():
            return str(int(value))

        return str(value).strip()

    text = str(value).strip()

    if text.lower() == "nan":
        return ""

    return text