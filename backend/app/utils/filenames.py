from backend.app import config


def normalize_cod_estab(cod_estab: str) -> str:
    solo_numeros = "".join(filter(str.isdigit, cod_estab))
    return solo_numeros.zfill(7)[:7]


def normalize_ruc(ruc: str) -> str:
    return "".join(filter(str.isdigit, ruc))[:11]


def normalize_anio(anio: str) -> str:
    return "".join(filter(str.isdigit, anio))[:2]


def build_base_filename(
    ruc: str,
    cod_estab: str,
    mes: str,
    anio: str,
    tipo_proceso: str,
) -> str:
    ruc_normalizado = normalize_ruc(ruc)
    cod_estab_normalizado = normalize_cod_estab(cod_estab)
    anio_normalizado = normalize_anio(anio)

    tipo_proceso_normalizado = (
        tipo_proceso.strip()
        if tipo_proceso in config.TIPOS_PROCESO
        else "CARGA ARCHIVO"
    )

    return (
        f"{ruc_normalizado}_"
        f"{cod_estab_normalizado}_"
        f"{mes}_"
        f"{anio_normalizado}_"
        f"{tipo_proceso_normalizado}"
    )


def build_csv_filename(
    ruc: str,
    cod_estab: str,
    mes: str,
    anio: str,
    tipo_proceso: str,
) -> str:
    return f"{build_base_filename(ruc, cod_estab, mes, anio, tipo_proceso)}.csv"


def build_zip_filename(
    ruc: str,
    cod_estab: str,
    mes: str,
    anio: str,
    tipo_proceso: str,
) -> str:
    return f"{build_base_filename(ruc, cod_estab, mes, anio, tipo_proceso)}.zip"


def build_report_filename(
    prefix: str,
    base_filename: str,
    extension: str = "ods",
) -> str:
    extension = extension.lstrip(".")
    return f"{prefix}_{base_filename}.{extension}"