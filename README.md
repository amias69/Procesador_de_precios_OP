# Observatorio de Precios

> Generador de archivos para el **Observatorio de Precios de DIGEMID**.

Una aplicación web diseñada para automatizar la generación de archivos compatibles con el sistema de carga masiva del Observatorio de Precios, a partir de la lista de precios de una oficina farmacéutica.

---

## Estado del proyecto

🧪 Beta

La aplicación se encuentra en fase beta. El flujo principal ya está completamente implementado y es funcional, mientras continúan realizándose mejoras de estabilidad, documentación y experiencia de usuario.

---

## ¿Por qué existe este proyecto?

El proceso de preparar un archivo para el Observatorio de Precios suele implicar tareas repetitivas:

- revisar registros sanitarios;
- validar precios;
- cruzar información con el catálogo oficial;
- generar el archivo final con el formato correcto;
- identificar productos descartados o con errores.

Este proyecto nace con un objetivo muy concreto:

> Automatizar ese proceso para que cualquier establecimiento farmacéutico pueda generar su archivo de carga de forma rápida, confiable y con la menor intervención manual posible.

La aplicación no busca reemplazar el criterio del usuario; busca eliminar el trabajo repetitivo para que este pueda concentrarse en verificar la información realmente importante.

---

## Características principales

- Descarga automática del catálogo oficial del Observatorio de Precios.
- Limpieza y preparación del catálogo para su utilización.
- Procesamiento de archivos Excel (.xlsx) y LibreOffice Calc (.ods).
- Validación de registros sanitarios.
- Validación de precios.
- Generación del archivo CSV compatible con el Observatorio de Precios.
- Generación automática del archivo ZIP final.
- Reportes de productos válidos, descartados y errores de precio.
- Interfaz web moderna y responsiva.
- Despliegue mediante Docker.

---

## Construido con

La aplicación fue desarrollada utilizando tecnologías modernas, ligeras y ampliamente adoptadas en el ecosistema Python y desarrollo web.

| Tecnología | Descripción |
|------------|-------------|
| Python | Lenguaje principal del proyecto. |
| FastAPI | API y servidor web. |
| Pandas | Procesamiento y transformación de datos. |
| OpenPyXL | Lectura de archivos Excel (.xlsx). |
| HTML, CSS y JavaScript | Interfaz web responsiva sin frameworks. |
| Docker & Docker Compose | Empaquetado y despliegue reproducible. |
| ODFPy | Lectura de archivos LibreOffice Calc (.ods). |

---

## Instalación

### Requisitos

- Docker
- Docker Compose

Clonar el repositorio:

```bash
git clone https://github.com/USUARIO/observatorio-precios.git
cd observatorio-precios
```

Construir e iniciar la aplicación:

```bash
docker compose up --build
```

Una vez iniciada, la aplicación estará disponible en:

http://localhost:8000

## Uso

El flujo de trabajo fue diseñado para que el usuario solo tenga que seguir una secuencia lógica de pasos.

   1. Completar los datos del establecimiento.
   2. Descargar o actualizar el catálogo oficial.
   3. Seleccionar el archivo Excel de la farmacia.
   4. Procesar la información.
   5. Descargar el archivo final y los reportes generados.

Todo el proceso se realiza desde una única interfaz web, sin necesidad de instalar software adicional ni manipular archivos manualmente durante el procesamiento.

---

## Documentación para el usuario

- 📘 Preparación del archivo Excel

---

## Arquitectura

La aplicación sigue una arquitectura modular que separa claramente la interfaz de usuario, la lógica de negocio y el procesamiento de datos.

```text
                    Usuario
                        │
                        ▼
               Interfaz Web (Frontend)
                        │
                        ▼
                 FastAPI (Backend)
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Descarga        Procesamiento      Validaciones
 del catálogo       de datos
        │               │
        └───────────────┼────────────────┘
                        ▼
              Generación de reportes
                        │
                        ▼
             Archivo final compatible
        con el Observatorio de Precios
```

La arquitectura completa del proyecto, así como la organización de carpetas y responsabilidades de cada componente, se encuentra documentada en:

- 📄 [Estructura del proyecto](docs/desarrollo/estructura_proyecto.md)

---

## Documentación

Además del código fuente, este proyecto mantiene una documentación técnica que describe las decisiones de diseño, el flujo de negocio y la arquitectura general.

- 📜 [Manifiesto del proyecto](docs/desarrollo/manifiesto.md)

  Explica la filosofía, los objetivos y los principios que guiaron el desarrollo de la aplicación.

- 🔄 [Flujo de negocio](docs/desarrollo/flujo_negocio.md)

  Describe paso a paso el proceso completo, desde la actualización del catálogo oficial hasta la generación del archivo final.

- 🏗️ [Estructura del proyecto](docs/desarrollo/estructura_proyecto.md)

  Documenta la organización del código, las responsabilidades de cada módulo y la arquitectura de la aplicación.

- 📘 [Preparación del archivo Excel](docs/usuario/preparacion_excel.md)

  Explica cómo preparar correctamente la lista de precios antes del procesamiento.
---

## Principios del proyecto

Durante el desarrollo se tomaron decisiones orientadas a mantener una aplicación simple, mantenible y fácil de desplegar.

Algunos de esos principios son:

- Priorizar soluciones simples sobre soluciones complejas.
- Automatizar tareas repetitivas sin alterar el criterio del usuario.
- Mantener una arquitectura clara y desacoplada.
- Favorecer la reproducibilidad mediante Docker.
- Documentar las decisiones importantes del proyecto.
- Diseñar pensando primero en la experiencia del usuario.
- Construir una herramienta que resulte útil antes que impresionante.

---

## Roadmap

La primera versión del proyecto ya cubre el flujo principal de generación de archivos para el Observatorio de Precios. Sin embargo, el proyecto continúa evolucionando.

### Completado

- ✅ Interfaz web responsiva.
- ✅ Descarga automática del catálogo oficial.
- ✅ Procesamiento de archivos Excel.
- ✅ Validación de registros sanitarios.
- ✅ Validación de precios.
- ✅ Generación del archivo CSV.
- ✅ Generación del archivo ZIP.
- ✅ Reportes de procesamiento.
- ✅ Contenedorización con Docker.

### Próximamente

- ⬜ Despliegue en VPS.
- ⬜ Dominio propio y HTTPS.
- ⬜ Mejoras en la experiencia de usuario.
- ⬜ Optimización del procesamiento.
- ⬜ Nuevas validaciones.

---

## Licencia

Este proyecto se distribuye bajo la licencia **GNU Affero General Public License v3.0 (AGPL-3.0)**.

Esta licencia permite usar, estudiar, modificar y redistribuir el software. Si una versión modificada se ofrece como servicio a través de una red, su código fuente también debe ponerse a disposición de los usuarios bajo la misma licencia.

La elección es práctica: permitir que el proyecto pueda utilizarse y mejorarse libremente, asegurando al mismo tiempo que las mejoras realizadas sobre una aplicación web permanezcan disponibles para la comunidad.

Consulta el archivo [LICENSE](LICENSE) para conocer los términos completos.

---

## Autor

Proyecto desarrollado por **Amias Corp.**

Si este proyecto resulta útil para tu institución o deseas contribuir con nuevas ideas y mejoras, cualquier aporte será bienvenido.

Las contribuciones, reportes de errores y sugerencias ayudan a que la herramienta continúe evolucionando.

---

> _La tecnología cambia. El objetivo permanece._
>
> _Crear herramientas simples que permitan a las personas dedicar su tiempo a lo realmente importante._