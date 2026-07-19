const API_BASE_URL = "http://127.0.0.1:8000";


const rucInput = document.getElementById("ruc");
const codEstabInput = document.getElementById("cod-estab");
const mesSelect = document.getElementById("mes");
const anioInput = document.getElementById("anio");
const tipoProcesoSelect = document.getElementById("tipo-proceso");

const filenamePreview = document.getElementById("filename-preview");

const archivoExcelInput = document.getElementById("archivo-excel");
const fileInfo = document.getElementById("file-info");

const catalogoDetails = document.getElementById("catalogo-details");
const catalogoOriginalDetail = document.getElementById("catalogo-original-detail");
const catalogoLimpioDetail = document.getElementById("catalogo-limpio-detail");
const catalogoReadyDetail = document.getElementById("catalogo-ready-detail");
const catalogoDetailMessage = document.getElementById("catalogo-detail-message");
const catalogoDetailTitle =document.getElementById("catalogo-detail-title");
const uploadBox = document.querySelector(".upload-box");

const cargarCatalogoManualButton = document.getElementById("cargar-catalogo-manual");
const catalogoManualInput = document.getElementById("catalogo-manual-input");

const recordarDatosInput = document.getElementById("recordar-datos");

const actualizarCatalogoButton = document.getElementById(
  "actualizar-catalogo"
);

const verCatalogoButton = document.getElementById(
  "ver-catalogo"
);

const procesarArchivoButton = document.getElementById(
  "procesar-archivo"
);

const descargarCsvButton = document.getElementById(
  "descargar-csv"
);

const descargarZipButton = document.getElementById(
  "descargar-zip"
);

const descargarValidosButton = document.getElementById(
  "descargar-validos"
);

const descargarDescartadosButton = document.getElementById(
  "descargar-descartados"
);

const descargarErroresButton = document.getElementById(
  "descargar-errores"
);

const catalogoStatus = document.getElementById(
  "catalogo-status"
);

const validosCount = document.getElementById(
  "validos-count"
);

const descartadosCount = document.getElementById(
  "descartados-count"
);

const erroresCount = document.getElementById(
  "errores-count"
);

const archivoFinalNombre = document.getElementById(
  "archivo-final-nombre"
);

const systemMessage = document.getElementById(
  "system-message"
);


let archivosGenerados = {
  csv: null,
  zip: null,
  reporteValidos: null,
  reporteDescartados: null,
  reporteErrores: null,
};


function completarFechaActual() {
  const hoy = new Date();

  const mesActual = String(
    hoy.getMonth() + 1
  ).padStart(2, "0");

  const anioActual = String(
    hoy.getFullYear()
  ).slice(-2);

  mesSelect.value = mesActual;
  anioInput.value = anioActual;
}


function limpiarSoloNumeros(valor) {
  return valor.replace(/\D/g, "");
}


function normalizarCodEstab(valor) {
  const soloNumeros = limpiarSoloNumeros(valor);

  if (!soloNumeros) {
    return "";
  }

  return soloNumeros
    .padStart(7, "0")
    .slice(-7);
}


function obtenerNombreFinal(extension = "zip") {
  const ruc =
    limpiarSoloNumeros(rucInput.value) || "RUC";

  const codEstab =
    normalizarCodEstab(codEstabInput.value) || "CODEEFF";

  const mes =
    mesSelect.value || "MM";

  const anio =
    limpiarSoloNumeros(anioInput.value).slice(0, 2) || "AA";

  const tipoProceso =
    tipoProcesoSelect.value || "CARGA ARCHIVO";

  return (
    `${ruc}_${codEstab}_${mes}_` +
    `${anio}_${tipoProceso}.${extension}`
  );
}


function actualizarVistaPreviaNombre() {
  filenamePreview.textContent =
    obtenerNombreFinal("zip");
}


function limitarCampoNumerico(
  input,
  maxLength
) {
  input.value = limpiarSoloNumeros(
    input.value
  ).slice(0, maxLength);
}


function manejarCambioArchivo() {
  const archivo = archivoExcelInput.files[0];

  if (!archivo) {
    fileInfo.textContent =
      "Ningún archivo seleccionado.";

    return;
  }

  const tamanioKB = (
    archivo.size / 1024
  ).toFixed(1);

  fileInfo.textContent =
    `Archivo seleccionado: ${archivo.name} ` +
    `(${tamanioKB} KB)`;

  fileInfo.classList.remove(
    "is-confirmed"
  );

  void fileInfo.offsetWidth;

  fileInfo.classList.add(
    "is-confirmed"
  );

  setTimeout(() => {
    fileInfo.classList.remove(
      "is-confirmed"
    );
  }, 1200);
}

async function cargarCatalogoManual() {
  const archivo =
    catalogoManualInput.files[0];

  if (!archivo) {
    return;
  }

  catalogoDetails.hidden = true;

  cargarCatalogoManualButton.disabled =
    true;

  cargarCatalogoManualButton.textContent =
    "Procesando...";

  mostrarMensaje(
    "Procesando el catálogo seleccionado. " +
    "Por favor, espera unos momentos."
  );

  const formData =
    new FormData();

  formData.append(
    "archivo",
    archivo
  );

  try {
    const response = await fetch(
      `${API_BASE_URL}/catalogo/cargar-manual`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data =
      await response.json();

    if (!response.ok) {
      throw new Error(
        obtenerMensajeError(data)
      );
    }

    catalogoStatus.textContent =
      "Catálogo cargado correctamente";

    verCatalogoButton.disabled =
      false;

    mostrarMensajeExito(
      "Catálogo cargado y procesado correctamente. " +
      "Todo está listo y puedes continuar."
    );

  } catch (error) {
    mostrarMensajeError(
      error.message
    );

  } finally {
    cargarCatalogoManualButton.disabled =
      false;

    cargarCatalogoManualButton.textContent =
      "Cargar catálogo manualmente";

    catalogoManualInput.value = "";
  }
}

function mostrarMensaje(texto) {
  systemMessage.textContent = texto;
}


function mostrarMensajeError(texto) {
  systemMessage.textContent = texto;

  systemMessage.classList.remove(
    "is-success"
  );

  systemMessage.classList.add(
    "is-error"
  );
}


function mostrarMensajeExito(texto) {
  systemMessage.textContent = texto;

  systemMessage.classList.remove(
    "is-error"
  );

  systemMessage.classList.add(
    "is-success"
  );
}


function limpiarErroresFormulario() {
  const campos = [
    {
      input: rucInput,
      errorId: "ruc-error",
    },
    {
      input: codEstabInput,
      errorId: "cod-estab-error",
    },
    {
      input: anioInput,
      errorId: "anio-error",
    },
  ];

  campos.forEach(
    ({ input, errorId }) => {
      input.classList.remove(
        "is-invalid"
      );

      const errorElement =
        document.getElementById(
          errorId
        );

      if (errorElement) {
        errorElement.textContent = "";
      }
    }
  );

  const uploadBox =
    document.querySelector(
      ".upload-box"
    );

  const archivoError =
    document.getElementById(
      "archivo-error"
    );

  uploadBox.classList.remove(
    "is-invalid"
  );

  if (archivoError) {
    archivoError.textContent = "";
  }

  systemMessage.classList.remove(
    "is-error",
    "is-success"
  );
}


function marcarErrorCampo(
  input,
  errorId,
  mensaje
) {
  input.classList.add(
    "is-invalid"
  );

  const errorElement =
    document.getElementById(
      errorId
    );

  if (errorElement) {
    errorElement.textContent =
      mensaje;
  }
}


function marcarErrorArchivo(
  mensaje
) {
  const uploadBox =
    document.querySelector(
      ".upload-box"
    );

  const archivoError =
    document.getElementById(
      "archivo-error"
    );

  uploadBox.classList.add(
    "is-invalid"
  );

  if (archivoError) {
    archivoError.textContent =
      mensaje;
  }
}

function manejarArchivoSoltado(archivo) {
  if (!archivo) {
    return;
  }

  const extensionesPermitidas = [
    ".xlsx",
    ".xls",
    ".ods",
  ];

  const nombreArchivo =
    archivo.name.toLowerCase();

  const extensionValida =
    extensionesPermitidas.some(
      (extension) =>
        nombreArchivo.endsWith(extension)
    );

  if (!extensionValida) {
    marcarErrorArchivo(
      "El archivo debe ser .xlsx, .xls u .ods."
    );

    return;
  }

  const dataTransfer =
    new DataTransfer();

  dataTransfer.items.add(archivo);

  archivoExcelInput.files =
    dataTransfer.files;

  manejarCambioArchivo();

  uploadBox.classList.remove(
    "is-invalid"
  );

  document.getElementById(
    "archivo-error"
  ).textContent = "";
}

function validarFormularioAntesDeProcesar() {
  limpiarErroresFormulario();

  let esValido = true;

  const ruc =
    limpiarSoloNumeros(
      rucInput.value
    );

  const codEstab =
    limpiarSoloNumeros(
      codEstabInput.value
    );

  const anio =
    limpiarSoloNumeros(
      anioInput.value
    );

  const archivo =
    archivoExcelInput.files[0];

  if (ruc.length !== 11) {
    marcarErrorCampo(
      rucInput,
      "ruc-error",
      "El RUC debe tener exactamente 11 dígitos."
    );

    esValido = false;
  }

  if (codEstab.length !== 7) {
    marcarErrorCampo(
      codEstabInput,
      "cod-estab-error",
      "El código de establecimiento debe tener exactamente 7 dígitos."
    );

    esValido = false;
  }

  if (anio.length !== 2) {
    marcarErrorCampo(
      anioInput,
      "anio-error",
      "El año debe tener exactamente 2 dígitos."
    );

    esValido = false;
  }

  if (!archivo) {
    marcarErrorArchivo(
      "Debes seleccionar un archivo antes de procesar."
    );

    esValido = false;
  }

  if (!esValido) {
    mostrarMensajeError(
      "Hay campos pendientes o inválidos. " +
      "Corrígelos antes de continuar."
    );

    const primerError =
      document.querySelector(
        ".is-invalid"
      );

    if (primerError) {
      primerError.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }

    return false;
  }

  return true;
}


function obtenerMensajeError(data) {
  if (!data) {
    return "Ocurrió un error inesperado.";
  }

  if (Array.isArray(data.detail)) {
    return data.detail.join(" ");
  }

  if (typeof data.detail === "string") {
    return data.detail;
  }

  return "Ocurrió un error inesperado.";
}


async function consultarEstadoCatalogo() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/catalogo/estado`
    );

    if (!response.ok) {
      throw new Error(
        "No se pudo consultar el catálogo."
      );
    }

    const data = await response.json();

    if (data.listo_para_procesar) {
      catalogoStatus.textContent =
        "Catálogo listo para procesar";

      catalogoDetailTitle.textContent =
        "Catálogo correcto";

      escribirTexto(
        catalogoDetailMessage,
        "El catálogo oficial se descargó y procesó correctamente. " +
        "Puedes continuar sin problemas."
      );

      verCatalogoButton.disabled = false;

    } else {
      catalogoDetailTitle.textContent =
        "Catálogo no disponible";

      escribirTexto(
        catalogoDetailMessage,
        "No se encontró un catálogo oficial preparado. " +
        "Actualiza el catálogo para poder continuar."
      );

      verCatalogoButton.disabled = false;
    }

  } catch (error) {
    catalogoStatus.textContent =
      "No se pudo consultar el estado del catálogo.";

    catalogoDetailTitle.textContent =
      "No se pudo verificar el catálogo";

    catalogoDetailMessage.textContent =
      "Comprueba que el servidor esté funcionando e inténtalo nuevamente.";

    verCatalogoButton.disabled = false;
  }
}

async function actualizarCatalogo() {
  catalogoDetails.hidden = true;

  actualizarCatalogoButton.disabled =
    true;

  actualizarCatalogoButton.textContent =
    "Actualizando...";

  mostrarMensaje(
    "Actualizando el catálogo oficial. " +
    "La descarga y preparación pueden tardar unos momentos. " +
    "Por favor, espera y no cierres esta página."
  );

  try {
    const response = await fetch(
      `${API_BASE_URL}/catalogo/actualizar`,
      {
        method: "POST",
      }
    );

    const data =
      await response.json();

    if (!response.ok) {
      throw new Error(
        obtenerMensajeError(data)
      );
    }

    catalogoStatus.textContent =
      "Catálogo actualizado correctamente";

    verCatalogoButton.disabled =
      false;

    mostrarMensajeExito(
      "Catálogo actualizado correctamente. " +
      "Todo está listo y puedes continuar."
    );

  } catch (error) {
    mostrarMensajeError(
      error.message
    );

  } finally {
    actualizarCatalogoButton.disabled =
      false;

    actualizarCatalogoButton.textContent =
      "Actualizar catálogo";
  }
}

function guardarDatosEstablecimiento() {
  if (!recordarDatosInput.checked) {
    localStorage.removeItem(
      "datosEstablecimiento"
    );

    return;
  }

  const datos = {
    ruc: rucInput.value,
    codEstab: codEstabInput.value,
  };

  localStorage.setItem(
    "datosEstablecimiento",
    JSON.stringify(datos)
  );
}


function cargarDatosEstablecimiento() {
  const datosGuardados =
    localStorage.getItem(
      "datosEstablecimiento"
    );

  if (!datosGuardados) {
    return;
  }

  try {
    const datos =
      JSON.parse(datosGuardados);

    rucInput.value =
      datos.ruc || "";

    codEstabInput.value =
      datos.codEstab || "";

    recordarDatosInput.checked =
      true;

  } catch {
    localStorage.removeItem(
      "datosEstablecimiento"
    );
  }
}

//función para dar efecto de movimiento al mensaje del botón "ver detalle"
let intervaloEscritura = null;

function escribirTexto(
  elemento,
  texto,
  velocidad = 12
) {
  if (intervaloEscritura) {
    clearInterval(intervaloEscritura);
  }

  elemento.textContent = "";

  let indice = 0;

  intervaloEscritura = setInterval(() => {
    elemento.textContent +=
      texto.charAt(indice);

    indice++;

    if (indice >= texto.length) {
      clearInterval(intervaloEscritura);
      intervaloEscritura = null;
    }
  }, velocidad);
}


async function procesarArchivo() {
  if (
    !validarFormularioAntesDeProcesar()
  ) {
    return;
  }

  const archivo =
    archivoExcelInput.files[0];

  const formData =
    new FormData();

  formData.append(
    "archivo",
    archivo
  );

  formData.append(
    "ruc",
    rucInput.value
  );

  formData.append(
    "cod_estab",
    codEstabInput.value
  );

  formData.append(
    "mes",
    mesSelect.value
  );

  formData.append(
    "anio",
    anioInput.value
  );

  formData.append(
    "tipo_proceso",
    tipoProcesoSelect.value
  );

  procesarArchivoButton.disabled =
    true;

  procesarArchivoButton.textContent =
    "Procesando...";

  mostrarMensaje(
    "Procesando archivo. Esto puede tardar unos segundos..."
  );

  try {
    const response = await fetch(
      `${API_BASE_URL}/procesamiento/procesar`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data =
      await response.json();

    if (!response.ok) {
      throw new Error(
        obtenerMensajeError(data)
      );
    }

    validosCount.textContent =
      data.resumen.validos;

    descartadosCount.textContent =
      data.resumen.descartados;

    erroresCount.textContent =
      data.resumen.errores_precio;

    archivosGenerados.csv =
      data.archivo_final_csv;

    archivosGenerados.zip =
      data.archivo_final_zip;

    archivosGenerados.reporteValidos =
      data.reportes.validos || null;

    archivosGenerados.reporteDescartados =
      data.reportes.descartados || null;

    archivosGenerados.reporteErrores =
      data.reportes.errores_precio || null;

    descargarCsvButton.disabled =
      false;

    descargarZipButton.disabled =
      false;

    descargarValidosButton.disabled =
      !archivosGenerados.reporteValidos;

    descargarDescartadosButton.disabled =
      !archivosGenerados.reporteDescartados;

    descargarErroresButton.disabled =
      !archivosGenerados.reporteErrores;

    archivoFinalNombre.textContent =
      data.archivo_final_zip;

    mostrarMensajeExito(
      data.message
    );

  } catch (error) {
    mostrarMensajeError(
      error.message
    );

  } finally {
    procesarArchivoButton.disabled =
      false;

    procesarArchivoButton.textContent =
      "Procesar archivo";
  }
}


function descargarArchivoFinal(
  filename
) {
  if (!filename) {
    return;
  }

  const url =
    `${API_BASE_URL}/descargas/archivo/` +
    encodeURIComponent(filename);

  window.location.href = url;
}


function descargarReporte(
  filename
) {
  if (!filename) {
    return;
  }

  const url =
    `${API_BASE_URL}/descargas/reporte/` +
    encodeURIComponent(filename);

  window.location.href = url;
}


function registrarEventos() {
  rucInput.addEventListener(
    "input",
    () => {
      limitarCampoNumerico(
        rucInput,
        11
      );

      rucInput.classList.remove(
        "is-invalid"
      );

      document.getElementById(
        "ruc-error"
      ).textContent = "";

      actualizarVistaPreviaNombre();
    }
  );

  recordarDatosInput.addEventListener(
    "change",
    guardarDatosEstablecimiento
  );

  rucInput.addEventListener(
    "change",
    guardarDatosEstablecimiento
  );

  codEstabInput.addEventListener(
    "change",
    guardarDatosEstablecimiento
  );

  codEstabInput.addEventListener(
    "input",
    () => {
      limitarCampoNumerico(
        codEstabInput,
        7
      );

      codEstabInput.classList.remove(
        "is-invalid"
      );

      document.getElementById(
        "cod-estab-error"
      ).textContent = "";

      actualizarVistaPreviaNombre();
    }
  );

  cargarCatalogoManualButton.addEventListener(
    "click",
    () => {
      catalogoManualInput.click();
    } 
  );

  catalogoManualInput.addEventListener(
    "change",
    cargarCatalogoManual
  );

  mesSelect.addEventListener(
    "change",
    actualizarVistaPreviaNombre
  );

  anioInput.addEventListener(
    "input",
    () => {
      limitarCampoNumerico(
        anioInput,
        2
      );

      anioInput.classList.remove(
        "is-invalid"
      );

      document.getElementById(
        "anio-error"
      ).textContent = "";

      actualizarVistaPreviaNombre();
    }
  );

  tipoProcesoSelect.addEventListener(
    "change",
    actualizarVistaPreviaNombre
  );

  archivoExcelInput.addEventListener(
    "change",
    () => {
      manejarCambioArchivo();

      const uploadBox =
        document.querySelector(
          ".upload-box"
        );

      uploadBox.classList.remove(
        "is-invalid"
      );

      document.getElementById(
        "archivo-error"
      ).textContent = "";
    }
  );

  actualizarCatalogoButton.addEventListener(
    "click",
    actualizarCatalogo
  );

  verCatalogoButton.addEventListener(
    "click",
    async () => {
      await consultarEstadoCatalogo();
      catalogoDetails.hidden = !catalogoDetails.hidden;
    }
  );

  procesarArchivoButton.addEventListener(
    "click",
    procesarArchivo
  );

  descargarCsvButton.addEventListener(
    "click",
    () => {
      descargarArchivoFinal(
        archivosGenerados.csv
      );
    }
  );

  descargarZipButton.addEventListener(
    "click",
    () => {
      descargarArchivoFinal(
        archivosGenerados.zip
      );
    }
  );

  descargarValidosButton.addEventListener(
    "click",
    () => {
      descargarReporte(
        archivosGenerados.reporteValidos
      );
    }
  );

  descargarDescartadosButton.addEventListener(
    "click",
    () => {
      descargarReporte(
        archivosGenerados.reporteDescartados
      );
    }
  );

  descargarErroresButton.addEventListener(
    "click",
    () => {
      descargarReporte(
        archivosGenerados.reporteErrores
      );
    }
  );
  uploadBox.addEventListener(
    "dragover",
    (event) => {
      event.preventDefault();

      uploadBox.classList.add(
        "is-dragging"
      );
    }
  );

  uploadBox.addEventListener(
    "dragleave",
    () => {
      uploadBox.classList.remove(
        "is-dragging"
      );
    }
  );

  uploadBox.addEventListener(
    "drop",
    (event) => {
      event.preventDefault();

      uploadBox.classList.remove(
        "is-dragging"
      );

      const archivo =
        event.dataTransfer.files[0];

      manejarArchivoSoltado(
        archivo
      );
    }
  );
}


async function iniciarApp() {
  completarFechaActual();

  cargarDatosEstablecimiento();

  actualizarVistaPreviaNombre();

  registrarEventos();

  await consultarEstadoCatalogo();
}


document.addEventListener(
  "DOMContentLoaded",
  iniciarApp
);