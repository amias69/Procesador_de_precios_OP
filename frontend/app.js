const rucInput = document.getElementById("ruc");
const codEstabInput = document.getElementById("cod-estab");
const mesSelect = document.getElementById("mes");
const anioInput = document.getElementById("anio");
const tipoProcesoSelect = document.getElementById("tipo-proceso");

const filenamePreview = document.getElementById("filename-preview");

const archivoExcelInput = document.getElementById("archivo-excel");
const fileInfo = document.getElementById("file-info");

const actualizarCatalogoButton = document.getElementById("actualizar-catalogo");
const verCatalogoButton = document.getElementById("ver-catalogo");
const procesarArchivoButton = document.getElementById("procesar-archivo");

const systemMessage = document.getElementById("system-message");

function completarFechaActual() {
  const hoy = new Date();

  const mesActual = String(hoy.getMonth() + 1).padStart(2, "0");
  const anioActual = String(hoy.getFullYear()).slice(-2);

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

  return soloNumeros.padStart(7, "0").slice(-7);
}

function obtenerNombreFinal(extension = "zip") {
  const ruc = limpiarSoloNumeros(rucInput.value) || "RUC";
  const codEstab = normalizarCodEstab(codEstabInput.value) || "CODEEFF";
  const mes = mesSelect.value || "MM";
  const anio = limpiarSoloNumeros(anioInput.value).slice(0, 2) || "AA";
  const tipoProceso = tipoProcesoSelect.value || "CARGA ARCHIVO";

  return `${ruc}_${codEstab}_${mes}_${anio}_${tipoProceso}.${extension}`;
}

function actualizarVistaPreviaNombre() {
  filenamePreview.textContent = obtenerNombreFinal("zip");
}

function limitarCampoNumerico(input, maxLength) {
  input.value = limpiarSoloNumeros(input.value).slice(0, maxLength);
}

function manejarCambioArchivo() {
  const archivo = archivoExcelInput.files[0];

  if (!archivo) {
    fileInfo.textContent = "Ningún archivo seleccionado.";
    return;
  }

  const tamanioKB = (archivo.size / 1024).toFixed(1);

  fileInfo.textContent = `Archivo seleccionado: ${archivo.name} (${tamanioKB} KB)`;
}

function mostrarMensaje(texto) {
  systemMessage.textContent = texto;
}

function limpiarErroresFormulario() {
  const campos = [
    { input: rucInput, errorId: "ruc-error" },
    { input: codEstabInput, errorId: "cod-estab-error" },
    { input: anioInput, errorId: "anio-error" },
  ];

  campos.forEach(({ input, errorId }) => {
    input.classList.remove("is-invalid");
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
      errorElement.textContent = "";
    }
  });

  const uploadBox = document.querySelector(".upload-box");
  const archivoError = document.getElementById("archivo-error");

  uploadBox.classList.remove("is-invalid");
  if (archivoError) {
    archivoError.textContent = "";
  }

  systemMessage.classList.remove("is-error", "is-success");
}

function marcarErrorCampo(input, errorId, mensaje) {
  input.classList.add("is-invalid");
  const errorElement = document.getElementById(errorId);

  if (errorElement) {
    errorElement.textContent = mensaje;
  }
}

function marcarErrorArchivo(mensaje) {
  const uploadBox = document.querySelector(".upload-box");
  const archivoError = document.getElementById("archivo-error");

  uploadBox.classList.add("is-invalid");

  if (archivoError) {
    archivoError.textContent = mensaje;
  }
}

function mostrarMensajeError(texto) {
  systemMessage.textContent = texto;
  systemMessage.classList.remove("is-success");
  systemMessage.classList.add("is-error");
}

function mostrarMensajeExito(texto) {
  systemMessage.textContent = texto;
  systemMessage.classList.remove("is-error");
  systemMessage.classList.add("is-success");
}

function validarFormularioAntesDeProcesar() {
  limpiarErroresFormulario();

  let esValido = true;

  const ruc = limpiarSoloNumeros(rucInput.value);
  const codEstab = limpiarSoloNumeros(codEstabInput.value);
  const anio = limpiarSoloNumeros(anioInput.value);
  const archivo = archivoExcelInput.files[0];

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
    marcarErrorArchivo("Debes seleccionar un archivo Excel antes de procesar.");
    esValido = false;
  }

  if (!esValido) {
    mostrarMensajeError(
      "Hay campos pendientes o inválidos. Corrígelos antes de continuar."
    );
    return false;
  }

  mostrarMensajeExito(
    "Validación local correcta. El archivo está listo para enviarse al backend."
  );

  return true;
}

function prepararBotonesTemporales() {
  actualizarCatalogoButton.addEventListener("click", () => {
    mostrarMensaje("Próximamente: actualización del catálogo oficial.");
    systemMessage.classList.remove("is-error", "is-success");
  });

  verCatalogoButton.addEventListener("click", () => {
    mostrarMensaje("Próximamente: detalles del catálogo oficial.");
    systemMessage.classList.remove("is-error", "is-success");
  });

  procesarArchivoButton.addEventListener("click", () => {
    const formularioValido = validarFormularioAntesDeProcesar();

    if (!formularioValido) {
      return;
    }

    mostrarMensajeExito(
      "Validación local correcta. Próximamente: procesamiento del archivo Excel."
    );
  });
}

function registrarEventos() {
  rucInput.addEventListener("input", () => {
    limitarCampoNumerico(rucInput, 11);
    rucInput.classList.remove("is-invalid");
    document.getElementById("ruc-error").textContent = "";
    actualizarVistaPreviaNombre();
  });

  codEstabInput.addEventListener("input", () => {
    limitarCampoNumerico(codEstabInput, 7);
    codEstabInput.classList.remove("is-invalid");
    document.getElementById("cod-estab-error").textContent = "";
    actualizarVistaPreviaNombre();
  });

  mesSelect.addEventListener("change", actualizarVistaPreviaNombre);

  anioInput.addEventListener("input", () => {
    limitarCampoNumerico(anioInput, 2);
    anioInput.classList.remove("is-invalid");
    document.getElementById("anio-error").textContent = "";
    actualizarVistaPreviaNombre();
  });

  tipoProcesoSelect.addEventListener("change", actualizarVistaPreviaNombre);

  archivoExcelInput.addEventListener("change", () => {
    manejarCambioArchivo();

    const uploadBox = document.querySelector(".upload-box");
    uploadBox.classList.remove("is-invalid");
    document.getElementById("archivo-error").textContent = "";
  });
}

function iniciarApp() {
  completarFechaActual();
  actualizarVistaPreviaNombre();
  registrarEventos();
  prepararBotonesTemporales();
}

document.addEventListener("DOMContentLoaded", iniciarApp);