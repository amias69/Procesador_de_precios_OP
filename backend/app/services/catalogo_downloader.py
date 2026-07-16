from pathlib import Path

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


URL = "https://opm-digemid.minsa.gob.pe/"

TEXTOS_CATALOGO = [
    "Catálogo de Productos Farmacéuticos actualizado diariamente",
    "Pharmaceutical Products Catalog updated daily",
]


def cerrar_popups(page, intentos: int = 5) -> None:
    """
    Cierra ventanas emergentes informativas si aparecen.
    """
    for _ in range(intentos):
        try:
            page.get_by_role(
                "button",
                name="Cerrar",
            ).click(timeout=2000)

        except PlaywrightTimeoutError:
            break


def obtener_enlace_catalogo(page):
    """
    Busca el enlace de descarga del catálogo oficial.
    """
    for texto in TEXTOS_CATALOGO:
        enlace = page.get_by_text(
            texto,
            exact=True,
        )

        try:
            enlace.wait_for(
                state="visible",
                timeout=5000,
            )
            return enlace

        except PlaywrightTimeoutError:
            pass

    raise RuntimeError(
        "No se encontró el enlace de descarga del catálogo oficial."
    )


def descargar_catalogo(
    archivo_salida: str | Path,
    headless: bool = True,
) -> Path:
    """
    Descarga el catálogo actualizado de productos farmacéuticos
    desde el Observatorio de DIGEMID.

    Parámetros:
        archivo_salida:
            Ruta donde se guardará el archivo Excel.

        headless:
            True ejecuta Firefox oculto.
            False muestra el navegador para depuración.

    Retorna:
        Path con la ruta del archivo descargado.
    """
    archivo_salida = Path(archivo_salida)

    archivo_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(
            headless=headless,
        )

        context = browser.new_context(
            accept_downloads=True,
            locale="es-PE",
            extra_http_headers={
                "Accept-Language": "es-PE,es;q=0.9",
            },
        )

        page = context.new_page()

        try:
            page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            cerrar_popups(page)

            enlace_catalogo = obtener_enlace_catalogo(
                page
            )

            with page.expect_download(
                timeout=60000
            ) as download_info:
                enlace_catalogo.click()

            download = download_info.value

            download.save_as(
                archivo_salida
            )

            return archivo_salida

        finally:
            browser.close()