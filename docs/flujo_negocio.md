# Flujo de negocio

## Objetivo del sistema

Tomar un archivo Excel con la lista de precios de una farmacia o botica, validarlo contra el catálogo oficial del Observatorio de Precios y generar un archivo CSV compatible con la carga masiva del sistema.

---

## Alcance de esta primera versión

Esta versión del sistema está diseñada únicamente para:

- Oficinas farmacéuticas privadas.
- Un solo establecimiento por archivo.
- Generación de archivo final en formato CSV y ZIP.
- Validación de productos mediante el registro sanitario.
- Uso del catálogo oficial del Observatorio de Precios como fuente de validación.

---

## Entradas del sistema

El sistema necesita dos fuentes de información:

### 1. Catálogo oficial del Observatorio de Precios
Archivo Excel descargado desde la plataforma del observatorio.

Este catálogo será procesado por la aplicación para:
- limpiar encabezados y filas innecesarias;
- obtener los registros sanitarios válidos;
- obtener el `CodProd` correspondiente a cada producto.

### 2. Archivo Excel de la farmacia
Archivo preparado por el usuario con la lista de precios de su establecimiento.

Debe contener obligatoriamente estas columnas:

- `registro_sanitario`
- `precio_empaque`
- `precio_unidad`

Puede contener columnas adicionales, pero serán ignoradas.

---

## Datos solicitados al usuario

Antes de procesar el archivo, la aplicación solicitará:

- `RUC`
- `CodEstab`
- `Mes`
- `Año`
- `Tipo de proceso`

Estos datos se usarán principalmente para:

- validar la estructura del archivo final;
- generar el nombre del archivo de salida.

---

## Flujo general del proceso

### Paso 1: actualizar catálogo oficial
La aplicación permite descargar el catálogo oficial del Observatorio de Precios.

Una vez descargado:
- se guarda una copia del archivo original;
- se ejecuta el proceso de limpieza;
- se guarda una versión limpia lista para trabajar.

### Paso 2: cargar archivo Excel de la farmacia
El usuario selecciona su archivo Excel de precios.

La aplicación verifica que el archivo contenga las columnas obligatorias:

- `registro_sanitario`
- `precio_empaque`
- `precio_unidad`

Si falta alguna de estas columnas, el archivo será rechazado.

### Paso 3: validar datos básicos
La aplicación valida:

- que `RUC` tenga el formato esperado;
- que `CodEstab` tenga 7 dígitos;
- que los precios sean numéricos;
- que los precios sean mayores que 0;
- que no existan filas vacías o inválidas en las columnas críticas.

### Paso 4: cruce con el catálogo oficial
Por cada fila del archivo de la farmacia:

1. se toma el valor de `registro_sanitario`;
2. se busca ese valor dentro del catálogo oficial limpio;
3. si se encuentra coincidencia, se obtiene el valor de `CodProd`;
4. si no se encuentra coincidencia, el producto se descarta.

### Paso 5: clasificación de resultados
Luego del cruce, los registros se separan en tres grupos:

#### 1. Válidos
Productos que:
- tienen registro sanitario;
- fueron encontrados en el catálogo oficial;
- tienen precios válidos;
- pueden entrar al archivo final.

#### 2. Descartados
Productos que:
- no fueron encontrados en el catálogo oficial;
- tienen registro sanitario inválido o ausente;
- no deben formar parte del archivo final.

#### 3. Errores de precio
Productos que:
- sí existen en el catálogo oficial;
- pero tienen problemas en `precio_empaque` o `precio_unidad`;
- por ejemplo: precio vacío, precio 0 o valor no numérico.

---

## Construcción del archivo final

Los productos válidos se convierten al formato exigido por el Observatorio para oficinas farmacéuticas privadas.

### Estructura del archivo CSV final

```text
CodEstab,CodProd,Precio 1,Precio 2
```

## Reglas de construcción

- CodEstab se exporta como texto.
- CodEstab debe tener 7 caracteres, completando con ceros a la izquierda si hace falta.
- CodProd proviene del catálogo oficial.
- Precio 1 se toma de precio_empaque.
- Precio 2 se toma de precio_unidad.
- los precios se exportan con punto decimal;
- los precios se exportan con dos decimales;
- no se deben exportar precios iguales a 0;
- no se deben generar filas en blanco;
- no se deben generar columnas extra.

## Nombre del archivo final

El sistema generará automáticamente el nombre del archivo usando este formato:

```text
RUC_CODEEFF_MM_AA_TIPO
```
Ejemplo:

```text
10477706849_0113084_03_25_CARGA ARCHIVO
```

A partir de ese nombre se podrá descargar:

- un archivo .csv
- un archivo .zip que contenga el .csv

### Salidas del sistema

La aplicación generará cuatro resultados principales:

### 1. Archivo CSV final
Archivo listo para cargar en el Observatorio de Precios.

### 2. Archivo ZIP final
Versión comprimida del CSV final.

### 3. Reporte de válidos
Listado de productos que sí ingresaron al archivo final.

### 4. Reporte de descartados
Listado de productos que fueron excluidos por no coincidir con el catálogo oficial.

### 5. Reporte de errores de precio
Listado de productos que no pudieron entrar por errores en los precios.

##Reglas de negocio de esta versión

- Solo se procesa un establecimiento por archivo.
- No se soporta carga de varias sucursales en un mismo lote.
- No se soportan formatos para sector público.
- No se soportan formatos para laboratorios o droguerías.
- No se soporta carga manual producto por producto.
- La existencia de un registro sanitario en el archivo de la farmacia no garantiza su validez; siempre debe contrastarse contra el catálogo oficial.
- Los productos descartados deben poder revisarse y descargarse, aunque no formen parte del archivo final.

## Flujo resumido
Actualizar catálogo oficial  
↓  
Cargar archivo Excel de la farmacia  
↓  
Validar columnas obligatorias  
↓  
Validar datos del establecimiento  
↓  
Cruzar por registro sanitario con el catálogo oficial  
↓  
Clasificar resultados en válidos / descartados / errores de precio  
↓  
Generar CSV final  
↓  
Generar ZIP final  
↓  
Permitir descarga de reportes y archivo final