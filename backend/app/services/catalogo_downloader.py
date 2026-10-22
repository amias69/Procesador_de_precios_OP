from pathlib import Path
import os
import zipfile
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

TIMEOUT = (10, 50)

def cargar_proxies():
    archivo = Path(
        os.getenv("CATALOGO_PROXIES_FILE", "/app/config/proxies.txt")
    )

    if not archivo.is_file():
        print(f"No se encontró el archivo de proxies: {archivo}")
        return []

    return [
        linea.strip()
        for linea in archivo.read_text(encoding="utf-8").splitlines()
        if linea.strip() and not linea.lstrip().startswith("#")
    ]


def descargar_catalogo(archivo_salida: str | Path) -> Path:
    ruta_salida = Path(archivo_salida)
    """
    Descarga el catálogo oficial de productos farmacéuticos de DIGEMID.
    """
    print("Intentando descargar catálogo directamente...")

    proxies = [None] + cargar_proxies()
    errores = []

    for proxy in proxies:
        origen = proxy or "conexión directa"
        print(f"Probando: {origen}")

        try:
            with requests.Session() as sesion:
                sesion.trust_env = False

                if proxy:
                    sesion.proxies = {
                        "http": proxy,
                        "https": proxy,
                    }

                respuesta = sesion.post(
                    URL_CATALOGO,
                    headers=HEADERS,
                    json=PAYLOAD,
                    timeout=TIMEOUT,
                )
                respuesta.raise_for_status()

            # Los archivos XLSX son contenedores ZIP y comienzan con la firma "PK".
            # Esto evita guardar como Excel una página HTML de bloqueo de Cloudflare.
            if not respuesta.content.startswith(b"PK"):
                raise ValueError("La respuesta no parece ser un XLSX")

            with zipfile.ZipFile(
                __import__("io").BytesIO(respuesta.content)
            ) as excel:
                if excel.testzip() is not None:
                    raise ValueError("El archivo XLSX está dañado")

                if "xl/workbook.xml" not in excel.namelist():
                    raise ValueError("El archivo no contiene un libro Excel")

            ruta_salida.parent.mkdir(parents=True, exist_ok=True)

            temporal = ruta_salida.with_suffix(".tmp")
            temporal.write_bytes(respuesta.content)
            temporal.replace(ruta_salida)

            print(f"Catálogo descargado correctamente mediante: {origen}")
            print(f"Guardado en: {ruta_salida}")
            return ruta_salida

        except (
            requests.RequestException,
            ValueError,
            zipfile.BadZipFile,
            OSError,
        ) as error:
            print(f"Falló {origen}: {error}")
            errores.append(f"{origen}: {error}")

    raise RuntimeError(
        "No se pudo descargar el catálogo mediante ninguna conexión. "
        + " | ".join(errores)
    )

