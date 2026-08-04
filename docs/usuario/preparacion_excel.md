# Preparación del archivo Excel

> **Propósito:** Explicar cómo preparar correctamente la lista de precios antes de procesarla con la aplicación.

> [!IMPORTANT]
> La aplicación valida la estructura del archivo antes de iniciar el procesamiento. Si no cumple los requisitos descritos en esta guía, el archivo será rechazado.

---

## Formato del archivo

Actualmente la aplicación acepta los siguientes formatos:

- `.xlsx` (Microsoft Excel)
- `.ods` (LibreOffice Calc)

> [!TIP]
> Si utiliza LibreOffice Calc, se recomienda guardar el archivo en formato `.ods`. Si utiliza Microsoft Excel, utilice el formato `.xlsx`.
---

## Columnas obligatorias

El archivo debe contener las siguientes columnas:

| Columna | Obligatoria | Descripción |
|----------|:-----------:|-------------|
| `registro_sanitario` | ✅ | Registro sanitario del producto. |
| `precio_empaque` | ✅ | Precio de venta del empaque completo. |
| `precio_unidad` | ✅ | Precio de venta por unidad. |
| `unidades_por_empaque` | ✅ | Cantidad de unidades contenidas en cada empaque. |

> [!IMPORTANT]
> Los nombres de las columnas deben escribirse exactamente como aparecen en la tabla anterior.

---

## Formato de los datos

Cada columna debe contener el siguiente tipo de información:

| Columna | Tipo de dato | Ejemplo |
|----------|--------------|---------|
| `registro_sanitario` | Texto | `EN12345` |
| `precio_empaque` | Número decimal | `18.50` |
| `precio_unidad` | Número decimal | `1.85` |
| `unidades_por_empaque` | Número entero | `10` |

Los valores numéricos deben almacenarse como números y no como texto.

---

## Columnas adicionales

La aplicación permite que el archivo contenga columnas adicionales.

Estas columnas serán ignoradas durante el procesamiento y no afectan el resultado final.

Esto permite utilizar directamente listas de precios exportadas desde distintos sistemas sin necesidad de eliminar información adicional.

---

## Ejemplo

| registro_sanitario | precio_empaque | precio_unidad | unidades_por_empaque |
|--------------------|---------------:|--------------:|---------------------:|
| EN12345 | 18.50 | 1.85 | 10 |
| EE04012 | 7.20 | 0.60 | 12 |
| F123456 | 45.00 | 1.50 | 30 |

---

## Recomendaciones

Para obtener los mejores resultados se recomienda:

- Utilizar la primera fila para los encabezados.
- Mantener un único producto por fila.
- Evitar filas completamente vacías entre los registros.
- No modificar los nombres de las columnas obligatorias.
- Revisar previamente que los precios sean correctos.

> [!IMPORTANT]
> Para garantizar un procesamiento correcto, utilice los nombres de las columnas exactamente como aparecen en esta guía. Se recomienda mantenerlos en minúsculas y utilizar guiones bajos (`_`) para separar las palabras.
---

## Próximamente

En futuras versiones la aplicación incluirá una plantilla descargable con la estructura recomendada para facilitar la preparación del archivo.