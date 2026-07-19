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
    archivo_salida: str = "catalogoproductos.xlsx",
) -> Path:

    print("Descargando catálogo...")

    respuesta = requests.post(
        URL_CATALOGO,
        headers=HEADERS,
        json=PAYLOAD,
        timeout=120,
    )

    respuesta.raise_for_status()

    # Un XLSX es internamente un ZIP.
    if not respuesta.content.startswith(b"PK"):
        raise RuntimeError(
            "La respuesta recibida no parece ser un archivo Excel válido."
        )

    ruta_salida = Path(archivo_salida)

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta_salida.write_bytes(
        respuesta.content
    )

    print(f"Catálogo guardado en: {ruta_salida}")

    return ruta_salida


if __name__ == "__main__":
    descargar_catalogo()
