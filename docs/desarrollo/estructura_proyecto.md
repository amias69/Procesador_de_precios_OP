# Estructura del proyecto

> **Propósito:** Describir la organización del proyecto, la arquitectura utilizada y la responsabilidad de cada uno de sus componentes.

> [!NOTE]
> Este documento describe **cómo está construido** el proyecto. El comportamiento funcional de la aplicación se documenta en el flujo de negocio.

---

## Arquitectura

La aplicación sigue una arquitectura cliente-servidor, separando claramente la interfaz de usuario, la lógica de negocio y el procesamiento de datos.

Cada componente posee una responsabilidad específica, facilitando el mantenimiento, la escalabilidad y la incorporación de nuevas funcionalidades sin afectar el resto del sistema.

```mermaid
flowchart LR

    U[Usuario]

    F[Frontend]

    B[Backend]

    D[Datos temporales]

    U --> F

    F --> B

    B --> D
```

---

## Organización del proyecto

El proyecto se encuentra dividido en dos componentes principales:

- **Frontend:** interfaz web utilizada por el usuario.
- **Backend:** procesamiento, validaciones y generación de archivos.

La estructura principal es la siguiente:

```text
observatorio-precios/

├── backend/
├── frontend/
├── docs/
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Backend

El backend fue desarrollado utilizando **FastAPI** y concentra toda la lógica de negocio de la aplicación.

Su organización busca mantener separadas las responsabilidades de cada módulo.

```text
backend/

app/

├── routes/
├── services/
├── validators/
├── utils/
├── data/
├── config.py
└── main.py
```

### Responsabilidades

| Componente | Responsabilidad |
|------------|-----------------|
| `routes` | Define los endpoints de la API. |
| `services` | Implementa la lógica de negocio y el procesamiento de datos. |
| `validators` | Valida la información proporcionada por el usuario. |
| `utils` | Funciones auxiliares utilizadas por distintos módulos. |
| `data` | Almacenamiento temporal de archivos durante el procesamiento. |
| `config.py` | Configuración general de la aplicación. |
| `main.py` | Punto de entrada del servidor FastAPI. |

---

## Frontend

El frontend corresponde a una aplicación web ligera desarrollada con HTML, CSS y JavaScript.

Su responsabilidad consiste en:

- Guiar al usuario durante el proceso.
- Validar información básica antes del envío.
- Mostrar el estado del procesamiento.
- Gestionar la descarga de los archivos generados.

Toda la lógica de negocio permanece en el backend.

---

## Datos temporales

Durante el procesamiento la aplicación utiliza directorios temporales para almacenar archivos intermedios.

```text
backend/data/

├── uploads/
├── outputs/
├── reports/
├── sessions/
└── catalogo/
```

Estos archivos no forman parte de la información permanente del sistema y son eliminados automáticamente para mantener un entorno de trabajo limpio.

---

## Contenedorización

La aplicación se distribuye mediante Docker.

El contenedor incluye todas las dependencias necesarias para ejecutar el proyecto de forma reproducible, evitando diferencias entre entornos de desarrollo y producción.

El despliegue se realiza mediante Docker Compose, simplificando la construcción, ejecución y actualización de la aplicación.

---

## Principios de organización

La estructura del proyecto fue diseñada siguiendo algunos principios fundamentales:

- Separación clara de responsabilidades.
- Organización modular.
- Baja dependencia entre componentes.
- Facilidad de mantenimiento.
- Escalabilidad.
- Simplicidad en la estructura del proyecto.

Cada directorio tiene una única responsabilidad y cada módulo cumple una función claramente definida, favoreciendo un código más legible y fácil de mantener a largo plazo.