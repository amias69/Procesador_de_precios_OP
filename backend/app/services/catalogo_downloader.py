from pathlib import Path

import requests

URL_CATALOGO = (
    "https://ms-opm.minsa.gob.pe/"
    "msopmcovid/producto/catalogoproductos"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:152.0) "
        "Gecko/20100101 Firefox/152.0"
    ),
    "Content-Type": "application/json",
    "Origin": "https://opm-digemid.minsa.gob.pe",
    "Referer": "https://opm-digemid.minsa.gob.pe/",
}

PAYLOAD = {
    "filtro": {
        "situacion": "ACT",
        "tokenGoogle": "",
    }
}

def descargar_catalogo(
    archivo_salida: str | Path,
) -> Path:
    """
    Descarga el catálogo oficial de productos farmacéuticos de DIGEMID.
    """

    ruta_salida = Path(archivo_salida)

    print("Descargando catálogo de productos farmacéuticos...")

    try:
        respuesta = requests.post(
            URL_CATALOGO,
            headers=HEADERS,
            json=PAYLOAD,
            timeout=120,
        )

        respuesta.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"No se pudo descargar el catálogo de DIGEMID: {error}"
        ) from error

    # Los archivos XLSX son contenedores ZIP y comienzan con la firma "PK".
    # Esto evita guardar como Excel una página HTML de bloqueo de Cloudflare.
    if not respuesta.content.startswith(b"PK"):
        raise RuntimeError(
            "DIGEMID respondió correctamente a la petición, "
            "pero la respuesta recibida no parece ser un archivo Excel válido."
        )

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta_salida.write_bytes(
        respuesta.content
    )

    print(f"Catálogo guardado en: {ruta_salida}")

    return ruta_salida