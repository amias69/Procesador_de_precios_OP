from backend.app import config


def only_digits(value: str) -> str:
    return "".join(filter(str.isdigit, value or ""))


def validate_ruc(ruc: str) -> list[str]:
    errors = []
    ruc_digits = only_digits(ruc)

    if len(ruc_digits) != 11:
        errors.append("El RUC debe tener exactamente 11 dígitos.")

    return errors


def validate_cod_estab(cod_estab: str) -> list[str]:
    errors = []
    cod_estab_digits = only_digits(cod_estab)

    if len(cod_estab_digits) != 7:
        errors.append("El código de establecimiento debe tener exactamente 7 dígitos.")

    return errors


def validate_mes(mes: str) -> list[str]:
    errors = []

    if mes not in {f"{number:02d}" for number in range(1, 13)}:
        errors.append("El mes debe estar entre 01 y 12.")

    return errors


def validate_anio(anio: str) -> list[str]:
    errors = []
    anio_digits = only_digits(anio)

    if len(anio_digits) != 2:
        errors.append("El año debe tener exactamente 2 dígitos.")

    return errors


def validate_tipo_proceso(tipo_proceso: str) -> list[str]:
    errors = []

    if tipo_proceso not in config.TIPOS_PROCESO:
        errors.append("El tipo de proceso no es válido.")

    return errors


def validate_establecimiento_data(
    ruc: str,
    cod_estab: str,
    mes: str,
    anio: str,
    tipo_proceso: str,
) -> list[str]:
    errors = []

    errors.extend(validate_ruc(ruc))
    errors.extend(validate_cod_estab(cod_estab))
    errors.extend(validate_mes(mes))
    errors.extend(validate_anio(anio))
    errors.extend(validate_tipo_proceso(tipo_proceso))

    return errors