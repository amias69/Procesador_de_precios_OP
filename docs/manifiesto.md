# Manifiesto del Proyecto

## Nombre provisional

Generador de carga para el Observatorio de Precios

## Objetivo

Crear una herramienta simple, visual y confiable para convertir una lista de precios de una farmacia o botica en un archivo CSV compatible con el formato de carga masiva del Observatorio de Precios.

## Filosofía

Este proyecto sigue el principio KISS:

> Keep It Simple, Stupid.

La aplicación debe hacer una tarea concreta y hacerla bien.

## Alcance inicial

La primera versión estará enfocada únicamente en:

- Farmacias y boticas del sector privado.
- Un archivo por establecimiento.
- Carga masiva mediante archivo CSV.
- Cruce por registro sanitario contra el catálogo oficial.
- Generación de CSV y ZIP final.

## Fuera del alcance inicial

No se implementará en la primera versión:

- Usuarios y sesiones.
- Historial de cargas.
- Soporte para múltiples sucursales en un solo archivo.
- Formatos para sector público.
- Formatos para laboratorios o droguerías.
- Modo nocturno.
- Base de datos.
- Panel administrativo.

## Principios de diseño

- Interfaz clara y responsiva.
- Una pantalla principal con bloques amplios.
- Cada bloque debe representar un paso del proceso.
- El usuario debe saber qué hacer en todo momento.
- Los errores deben ser visibles y entendibles.
- Los archivos descartados no deben desaparecer silenciosamente.
- La aplicación debe poder correr localmente y también desplegarse en una VPS.

## Paleta de colores

- Azul noche: `#0B1D33`
- Azul profundo: `#123A5A`
- Azul medio: `#1F5A7A`
- Gris azulado: `#6B7C8A`
- Gris claro: `#D7DDE2`

## Columnas requeridas del Excel de entrada

El archivo Excel de la farmacia debe contener obligatoriamente estas columnas:

```text
registro_sanitario
precio_empaque
precio_unidad
```
Las columnas extra serán ignoradas.

## Formato final del CSV

El archivo final para farmacias y boticas privadas tendrá esta estructura:

```text
CodEstab,CodProd,Precio 1,Precio 2
```

Donde:

- CodEstab: código de establecimiento farmacéutico.
- CodProd: código del producto obtenido desde el catálogo oficial.
- Precio 1: precio por empaque.
- Precio 2: precio unitario.

Regla principal de validación

Solo entrarán al archivo final los productos cuyo registro sanitario exista en el catálogo oficial actualizado del Observatorio de Precios.

Los productos sin coincidencia serán descartados y reportados.