Estructura del proyecto
Objetivo de la estructura

Organizar el proyecto de forma clara, modular y escalable, manteniendo la filosofía KISS.

La idea es separar visualmente:

    la interfaz;

    la lógica del backend;

    las validaciones;

    los procesos de lectura y generación de archivos;

    la documentación del proyecto;

    los archivos temporales y de salida.

La aplicación debe poder ejecutarse localmente y también ser desplegable en una VPS sin reestructurar el proyecto.
Árbol general del proyecto

observatorio-precios/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── catalogo_routes.py
│   │   │   ├── descarga_routes.py
│   │   │   └── procesamiento_routes.py
│   │   ├── services/
│   │   │   ├── catalogo_cleaner.py
│   │   │   ├── catalogo_downloader.py
│   │   │   ├── csv_generator.py
│   │   │   ├── excel_reader.py
│   │   │   ├── processor.py
│   │   │   └── zip_generator.py
│   │   ├── utils/
│   │   │   ├── filenames.py
│   │   │   └── paths.py
│   │   └── validators/
│   │       ├── establecimiento_validator.py
│   │       ├── excel_validator.py
│   │       └── precio_validator.py
│   ├── data/
│   │   ├── catalogo_limpio/
│   │   ├── catalogo_original/
│   │   ├── outputs/
│   │   ├── reports/
│   │   └── uploads/
│   └── requirements.txt
├── docs/
│   ├── estructura_proyecto.md
│   ├── flujo_negocio.md
│   └── manifiesto.md
├── frontend/
│   ├── app.js
│   ├── assets/
│   │   └── icons/
│   ├── index.html
│   ├── manifest.json
│   ├── service-worker.js
│   └── styles.css
├── README.md
└── run.py

Descripción por carpeta
backend/

Contiene toda la lógica del lado del servidor.

Aquí viven:

    la API de FastAPI;

    la lectura y procesamiento de archivos;

    las validaciones;

    la generación del CSV y ZIP;

    la lógica de negocio principal.

Esta carpeta no debe contener elementos visuales de la interfaz.
backend/app/

Es el corazón del backend.

Aquí se agrupan:

    configuración general;

    rutas de la API;

    servicios;

    validadores;

    utilidades.

backend/app/main.py

Punto de entrada del backend.
Responsabilidades

    crear la aplicación FastAPI;

    registrar las rutas;

    configurar CORS si es necesario;

    servir el frontend si decidimos integrarlo desde FastAPI;

    exponer la API para uso local o despliegue en VPS.

backend/app/config.py

Archivo de configuración general del backend.
Responsabilidades posibles

    definir rutas base del proyecto;

    definir nombres de carpetas de trabajo;

    parámetros globales de la aplicación;

    extensiones permitidas;

    valores por defecto para exportación.

No debe contener lógica de negocio.
Carpeta backend/app/routes/

Aquí se definen los endpoints de la API.
Las rutas solo reciben solicitudes, validan lo mínimo necesario y delegan la lógica a los servicios.

No deben contener procesamiento pesado.
catalogo_routes.py

Responsable de las acciones relacionadas con el catálogo oficial.
Ejemplos de responsabilidades

    actualizar o descargar el catálogo;

    consultar el estado del catálogo;

    devolver información sobre la última actualización;

    disparar el proceso de limpieza del catálogo.

procesamiento_routes.py

Responsable del flujo principal de procesamiento del archivo de precios.
Ejemplos de responsabilidades

    recibir el archivo Excel de la farmacia;

    recibir los datos del establecimiento;

    lanzar el procesamiento;

    devolver el resumen de válidos, descartados y errores.

descarga_routes.py

Responsable de la descarga de resultados.
Ejemplos de responsabilidades

    descargar CSV final;

    descargar ZIP final;

    descargar reporte de válidos;

    descargar reporte de descartados;

    descargar reporte de errores de precio.

Carpeta backend/app/services/

Aquí vive la lógica operativa real del sistema.
Los servicios deben ser reutilizables y estar lo más desacoplados posible de la capa web.
catalogo_downloader.py

Responsable de descargar el catálogo oficial desde el Observatorio de Precios.
Funciones esperadas

    conectarse a la fuente oficial;

    descargar el archivo Excel;

    guardarlo en backend/data/catalogo_original/.

catalogo_cleaner.py

Responsable de limpiar el catálogo oficial descargado.
Funciones esperadas

    eliminar encabezados y filas basura;

    conservar únicamente las columnas necesarias;

    dejar el catálogo listo para buscar registros sanitarios y obtener CodProd;

    guardar el resultado en backend/data/catalogo_limpio/.

excel_reader.py

Responsable de leer archivos Excel de entrada.
Funciones esperadas

    abrir el archivo de la farmacia;

    leer columnas;

    normalizar nombres si fuera necesario;

    devolver la información en una estructura utilizable por el procesador.

processor.py

Es el núcleo del flujo de negocio.
Responsabilidades

    tomar el archivo de la farmacia ya leído;

    validar columnas obligatorias;

    validar precios;

    cruzar cada registro_sanitario contra el catálogo oficial limpio;

    clasificar los registros en válidos, descartados y errores;

    construir la estructura final que luego usará el generador de CSV;

    preparar los datos para reportes.

Este archivo será probablemente el más importante del backend.
csv_generator.py

Responsable de generar el archivo CSV final del observatorio.
Responsabilidades

    tomar los registros válidos;

    construir el CSV con el orden exacto:

        CodEstab

        CodProd

        Precio 1

        Precio 2

    exportar con formato correcto;

    guardar el resultado en backend/data/outputs/.

zip_generator.py

Responsable de generar el archivo ZIP final.
Responsabilidades

    tomar el CSV ya generado;

    comprimirlo en un ZIP;

    guardarlo en backend/data/outputs/.

Carpeta backend/app/validators/

Contiene validaciones separadas por responsabilidad.
La idea es no mezclar reglas de negocio con validaciones básicas de formato.
establecimiento_validator.py

Responsable de validar los datos del establecimiento.
Ejemplos de validación

    RUC con longitud correcta;

    CodEstab con 7 dígitos;

    mes válido;

    año válido;

    tipo de proceso válido.

excel_validator.py

Responsable de validar la estructura del Excel de la farmacia.
Ejemplos de validación

    existencia de columnas obligatorias:

        registro_sanitario

        precio_empaque

        precio_unidad

    archivo legible;

    archivo no vacío;

    extensión permitida.

precio_validator.py

Responsable de validar precios.
Ejemplos de validación

    valores numéricos;

    precios mayores que 0;

    manejo de nulos o cadenas vacías;

    formateo a dos decimales si corresponde.

Carpeta backend/app/utils/

Contiene utilidades transversales que no son lógica de negocio principal, pero ayudan a organizar el sistema.
filenames.py

Responsable de construir nombres de archivos.
Ejemplos

    nombre del CSV final;

    nombre del ZIP final;

    nombre de reportes;

    limpieza de nombres si hiciera falta.

paths.py

Responsable de centralizar rutas del proyecto.
Ejemplos

    ruta del catálogo original;

    ruta del catálogo limpio;

    ruta de uploads;

    ruta de outputs;

    ruta de reports.

Esto evita escribir rutas hardcodeadas en varios archivos.
Carpeta backend/data/

Contiene los archivos con los que trabaja el sistema.

No contiene código.
backend/data/catalogo_original/

Guarda el archivo descargado desde el Observatorio de Precios sin modificar.

Su función es conservar una copia fuente.
backend/data/catalogo_limpio/

Guarda la versión procesada del catálogo oficial.

Esta es la versión que utilizará el sistema para el cruce por registro_sanitario.
backend/data/uploads/

Guarda temporalmente los archivos Excel subidos por el usuario.

Si más adelante se decide procesar en memoria y no guardar archivos, esta carpeta podrá cambiar de uso, pero por ahora se mantiene porque simplifica el flujo.
backend/data/outputs/

Guarda los archivos finales generados por el sistema.
Ejemplos

    CSV final;

    ZIP final.

backend/data/reports/

Guarda los reportes de procesamiento.
Ejemplos

    reporte de válidos;

    reporte de descartados;

    reporte de errores de precio.

backend/requirements.txt

Lista de dependencias del backend.

Aquí irán las librerías necesarias para:

    FastAPI;

    lectura de Excel;

    procesamiento de datos;

    servidor ASGI;

    generación de archivos.

Carpeta frontend/

Contiene toda la interfaz del usuario.

Aquí vive la parte visual de la aplicación:

    estructura HTML;

    estilos CSS;

    comportamiento del frontend con JavaScript;

    recursos para PWA.

La idea es mantener esta capa lo más simple posible, con JavaScript nativo y sin frameworks en esta primera versión.
frontend/index.html

Archivo principal de la interfaz.
Responsabilidades

    definir la estructura visual de la pantalla;

    contener los bloques principales de la app;

    servir como punto de montaje del frontend.

Se espera que contenga al menos estas secciones:

    encabezado;

    datos del establecimiento;

    catálogo oficial;

    carga de archivo;

    procesamiento;

    resultados;

    descargas finales.

frontend/styles.css

Archivo principal de estilos.
Responsabilidades

    aplicar la paleta visual del proyecto;

    construir la interfaz responsive;

    definir tarjetas, botones, formularios y estados visuales;

    adaptar la experiencia a escritorio y móvil;

    dar formato a la app como PWA instalable.

frontend/app.js

Lógica del frontend.
Responsabilidades

    capturar formularios;

    gestionar la carga de archivos;

    comunicarse con el backend;

    actualizar la interfaz con el resultado del procesamiento;

    mostrar mensajes, errores y estados;

    activar descargas.

frontend/manifest.json

Configuración de la PWA.
Responsabilidades

    nombre de la app;

    color del tema;

    color de fondo;

    iconos;

    comportamiento al instalar la app en escritorio o móvil.

frontend/service-worker.js

Base para comportamiento PWA.

En la primera versión puede ser mínimo.
Responsabilidades posibles

    cachear archivos estáticos;

    permitir instalación;

    mejorar la experiencia offline si más adelante se decide.

frontend/assets/icons/

Carpeta para iconos de la PWA y otros recursos gráficos.
Carpeta docs/

Contiene la documentación viva del proyecto.
Sirve como mapa antes de programar y como referencia cuando el proyecto crezca.
docs/manifiesto.md

Contiene la filosofía, objetivos, límites y principios del proyecto.

Es el documento que define qué estamos construyendo y qué no.
docs/flujo_negocio.md

Describe el flujo real del proceso de negocio.

Debe responder preguntas como:

    qué entra al sistema;

    qué se valida;

    cómo se cruzan los datos;

    qué se genera al final.

docs/estructura_proyecto.md

Este documento.
Define el propósito de cada carpeta y archivo principal.
README.md

Documento general del proyecto.

Más adelante puede incluir:

    descripción de la app;

    requisitos;

    cómo ejecutar el proyecto;

    estructura general;

    dependencias.

run.py

Lanzador local del proyecto.

Su objetivo futuro será simplificar la ejecución en entorno local.

Por ejemplo:

    levantar el backend;

    abrir el navegador automáticamente;

    preparar el entorno local de la aplicación.

No es obligatorio usarlo desde el primer día, pero queda reservado como punto de arranque cómodo para el usuario final o para desarrollo local.
Criterios de arquitectura
1. Separación clara de responsabilidades

Cada archivo debe tener una función clara.
Si un archivo empieza a hacer demasiadas cosas, hay que dividirlo.
2. Backend orientado a servicios

La lógica importante no debe quedar enterrada dentro de las rutas.
3. Frontend simple

La interfaz debe resolverse con HTML, CSS y JavaScript nativo en esta primera versión.
4. Despliegue flexible

La misma estructura debe servir para:

    ejecución local;

    despliegue en VPS.

5. KISS

No agregar carpetas, capas o abstracciones solo “por si acaso”.
Cada pieza debe justificar su existencia.
Orden recomendado de construcción
Fase 1: documentación

    docs/manifiesto.md

    docs/flujo_negocio.md

    docs/estructura_proyecto.md

Fase 2: interfaz base

    frontend/index.html

    frontend/styles.css

    frontend/app.js

Fase 3: backend mínimo

    backend/app/main.py

    backend/app/config.py

    backend/app/utils/paths.py

    backend/app/utils/filenames.py

Fase 4: validaciones

    backend/app/validators/establecimiento_validator.py

    backend/app/validators/excel_validator.py

    backend/app/validators/precio_validator.py

Fase 5: procesamiento

    backend/app/services/excel_reader.py

    backend/app/services/processor.py

    backend/app/services/csv_generator.py

    backend/app/services/zip_generator.py

Fase 6: catálogo oficial

    backend/app/services/catalogo_downloader.py

    backend/app/services/catalogo_cleaner.py

Fase 7: rutas

    backend/app/routes/catalogo_routes.py

    backend/app/routes/procesamiento_routes.py

    backend/app/routes/descarga_routes.py

Fase 8: PWA y remates

    frontend/manifest.json

    frontend/service-worker.js

    iconos

    run.py

    README.md