from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    page.goto(
        "https://opm-digemid.minsa.gob.pe/#/consulta-producto",
        wait_until="domcontentloaded",
        timeout=60000,
    )
    page.wait_for_timeout(8000)

    while page.locator("ngb-modal-window").count() > 0:
        try:
            page.locator("ngb-modal-window button", has_text="Cerrar").first.click(timeout=5000)
            page.wait_for_timeout(1000)
            print("Popup cerrado")
        except Exception as exc:
            print(f"No se pudo cerrar popup: {exc}")
            break

    print("Modales visibles:", page.locator("ngb-modal-window").count())

    print("Clicking catalog link...")
    with page.expect_download(timeout=60000) as download_info:
        page.get_by_text("Pharmaceutical Products Catalog updated daily").click()

    download = download_info.value
    print("suggested:", download.suggested_filename)
    download.save_as("catalogoproductos_test.xlsx")
    print("saved catalogoproductos_test.xlsx")

    browser.close()
