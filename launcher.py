import threading
import time
import urllib.request
import webbrowser

import uvicorn

from backend.app.main import app


HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"


def servidor_esta_activo() -> bool:
    try:
        with urllib.request.urlopen(
            URL,
            timeout=1,
        ):
            return True

    except Exception:
        return False


def abrir_navegador() -> None:
    time.sleep(1.5)
    webbrowser.open(URL)


def main() -> None:
    # Si ya hay una instancia funcionando,
    # simplemente vuelve a abrir la interfaz.
    if servidor_esta_activo():
        webbrowser.open(URL)
        return

    hilo_navegador = threading.Thread(
        target=abrir_navegador,
        daemon=True,
    )

    hilo_navegador.start()

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
    )


if __name__ == "__main__":
    main()