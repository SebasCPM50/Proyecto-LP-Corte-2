# MANUAL DE USUARIO — LENGUAJE ARCANUM

## INTRODUCCIÓN

Arcanum es un lenguaje de dominio específico (DSL) diseñado para facilitar tareas analíticas de preparación, transformación y exploración estadística de datos tabulares. 

El lenguaje adopta una temática alquímica intuitiva donde cada elemento de ciencia de datos tiene un equivalente:
* Un conjunto de datos (DataFrame) es una **Poción**
* Una columna o variable es un **Ingrediente**
* Un archivo de código es un **Grimorio**
* Una función reutilizable es una **Receta**
* Una librería de recetas es un **Compendio**

Este manual te guiará paso a paso para que aprendas a escribir, ejecutar y depurar tus propios análisis de datos en Arcanum.

---

## REQUISITOS Y EJECUCIÓN RÁPIDA

### Requisitos del sistema
Para ejecutar Arcanum necesitas únicamente:
* Python 3.10 o superior
* Java Runtime Environment (JRE) para el analizador sintáctico
* El paquete de Python `antlr4-python3-runtime==4.13.2`

### Cómo ejecutar un script
Para ejecutar cualquier archivo `.arc`, utiliza el comando principal desde la raíz del proyecto:

```bash
python3 src/main.py ruta/a/tu_archivo.arc
```

Si deseas ver el Árbol de Análisis Sintáctico (AST) generado por ANTLR para entender cómo el compilador interpretó tu código, añade la bandera `--arbol`:

```bash
python3 src/main.py ruta/a/tu_archivo.arc --arbol
```

---

## ESTRUCTURA DE UN GRIMORIO (.ARC)

Un programa de Arcanum se compone de hechizos (instrucciones) terminados en punto y coma (`;`). Los comentarios inician con el símbolo `#`:

```arc
# Esto es un comentario explicativo
datos = invocar desde "csv/ventas.csv";

limpios = sanar datos descartar_nulos;

revelar limpios;
```

---

## GUÍA DE OPERACIONES ANALÍTICAS

### 1. Cargar archivos CSV
Para cargar una tabla de datos desde un archivo en disco, utiliza la instrucción `invocar desde`:

```arc
ventas = invocar desde "csv/ventas.csv";
```
El motor de Arcanum infiere automáticamente si cada columna contiene números enteros, números decimales, booleanos, texto o valores nulos `None`.

### 2. Limpieza de datos y tratamiento de nulos
Es común que los datos reales tengan valores faltantes o celdas vacías. Arcanum ofrece dos formas de sanar tus datos:

* **Eliminar filas incompletas:** Descarta cualquier registro que contenga al menos una casilla vacía:
```arc
ventas_limpias = sanar ventas descartar_nulos;
```

* **Imputar valores por defecto:** Rellena los valores nulos de una columna específica sin borrar la fila:
```arc
ventas_rellenas = sanar ventas llenar descuento con 0.0;
```

### 3. Filtrar registros
Para conservar solo las filas que cumplen un criterio lógico, utiliza `purificar ... donde (...)`:

```arc
# Filtro simple
ventas_grandes = purificar ventas donde (unidades > 5);

# Filtro con operadores lógicos combinados (y, o, no)
filtradas = purificar ventas donde (ciudad == "Bogota" y (unidades >= 2 o precio > 100000));
```

### 4. Seleccionar columnas de interés
Si tu dataset tiene muchas columnas y solo necesitas algunas para tu reporte, usa `recolectar`:

```arc
reducidas = recolectar [fecha, ciudad, total] de ventas;
```

### 5. Crear columnas calculadas
Para calcular un nuevo valor a partir de los ingredientes existentes, usa `transmutar`:

```arc
con_subtotal = transmutar ventas con subtotal = unidades * precio_unitario;
con_total = transmutar con_subtotal con total = subtotal - (subtotal * descuento);
```

### 6. Ordenar datos
Para ordenar las filas según el valor de una columna, usa `ordenar`:

```arc
# Orden ascendente (de menor a mayor)
ordenadas_asc = ordenar ventas por precio asc;

# Orden descendente (de mayor a menor)
ordenadas_desc = ordenar ventas por total desc;
```
*Nota:* Los valores nulos `None` se colocan automáticamente al final para evitar errores de ordenamiento.

### 7. Agrupar y calcular resúmenes estadísticos
La operación `destilar` agrupa las filas por una o más categorías y calcula métricas sobre cada grupo:

```arc
resumen_ciudades = destilar ventas agrupar [ciudad] agregando [
    suma total como ingreso_total,
    media total como ticket_promedio,
    desviacion total como dispersion_ventas,
    contar como total_transacciones
];
```

Las funciones de agregación disponibles son:
* `suma`: Suma acumulada de valores numéricos
* `media`: Promedio aritmético muestral
* `mediana`: Valor central de los registros ordenados
* `desviacion`: Desviación estándar muestral
* `minimo`: Valor más bajo del grupo
* `maximo`: Valor más alto del grupo
* `contar`: Cantidad total de registros del grupo

### 8. Exploración estadística automática
Para ver un resumen completo de todas las columnas numéricas sin escribir fórmulas manuales, usa `describir`:

```arc
describir ventas;
```
Esto imprimirá en pantalla una tabla resumen con el conteo, media, desviación estándar, mínimo y máximo para cada columna numérica.

### 9. Generación de números aleatorios
Arcanum incluye un generador de azar integrado sin dependencias externas:

```arc
# Decimal entre 0.0 y 1.0
prob = random();

# Entero entre 0 y 100
porcentaje = random(100);

# Entero entre 1 y 6
dado = random(1, 6);
```

### 10. Visualización y guardado
* **Mostrar en terminal:** Para ver una poción completa con formato alineado, usa `revelar`:
```arc
revelar resumen_ciudades;
```

* **Exportar a archivo CSV:** Para guardar tu poción procesada en disco, usa `preservar`:
```arc
preservar resumen_ciudades en "salidas/resumen_ciudades.csv";
```

---

## USO DE COMPENDIOS Y RECETAS (LIBRERÍAS PROPIAS)

Arcanum cuenta con su propio sistema de módulos sin usar el comando `import` de Python:

### Cargar una librería existente
Para cargar recetas de la carpeta `compendios/`, usa `usar compendio`:

```arc
usar compendio matematicas;

# Invocamos la receta con el prefijo del compendio
subtotal = 200000;
iva = matematicas.calcular_iva(subtotal, 0.19);
total_con_iva = subtotal + iva;

revelar total_con_iva;
```

### Crear tus propias recetas
Puedes definir funciones reutilizables directamente en tu grimorio usando la palabra `receta`:

```arc
receta calcular_comision(monto, porcentaje) {
    comision = monto * porcentaje;
    devolver comision;
}

premio = calcular_comision(500000, 0.05);
```

---

## ERRORES COMUNES Y CÓMO RESOLVERLOS

Arcanum cuenta con un analizador semántico que detecta inconsistencias lógicas antes de producir cálculos erróneos:

### Variable no declarada
* **Error:** `[Error Semántico] Línea X: La variable o ingrediente 'tasa' no ha sido declarada o invocada previamente`
* **Solución:** Revisa que el nombre de la variable esté bien escrito y que haya sido asignada antes de utilizarla.

### Columna inexistente en la tabla
* **Error:** `[Error Semántico] Línea X: La poción 'ventas' no contiene el ingrediente (columna) 'costo'`
* **Solución:** Verifica los nombres exactos de las columnas en la cabecera de tu archivo CSV. El compilador te listará entre paréntesis las columnas que sí existen en la poción.

### Incompatibilidad de tipos
* **Error:** `[Error Semántico] Línea X: La variable 'descuento' es de tipo NUMERO, no es una POCIÓN (tabla de datos)`
* **Solución:** Ocurre si intentas aplicar una operación tabular (`recolectar`, `purificar`, `destilar`) sobre una variable que contiene un número o texto simple.

### División por cero
* **Error:** `[Error Semántico] Línea X: División por cero no permitida`
* **Solución:** Asegúrate de que el divisor en tus operaciones aritméticas o fórmulas calculadas sea diferente de cero.
