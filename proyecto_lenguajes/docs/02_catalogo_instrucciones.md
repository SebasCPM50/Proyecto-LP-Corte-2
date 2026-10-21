# Catálogo de Instrucciones — Arcanum (Segundo Corte)

## 1. Palabras reservadas

| Palabra clave | Significado | Equivalente conceptual en Data Science |
|---|---|---|
| `invocar` | Inicia la carga de un conjunto de datos desde un archivo | `pd.read_csv(...)` |
| `desde` | Indica la ruta de origen de un archivo o poción | `from` |
| `recolectar` | Selecciona un subconjunto de columnas (ingredientes) | `df[[col1, col2]]` |
| `de` | Enlace para indicar la poción fuente en `recolectar` | `from` / `of` |
| `purificar` | Filtra filas según condiciones booleanas | `df[condicion]` |
| `donde` | Introduce la condición de filtrado | `where` |
| `ordenar` | Ordena los registros según una columna | `df.sort_values(...)` |
| `por` | Introduce la columna o lista de agrupación/orden | `by` |
| `asc` / `ascendente` | Orden ascendente (de menor a mayor) | `ascending=True` |
| `desc` / `descendente` | Orden descendente (de mayor a menor) | `ascending=False` |
| `transmutar` | Crea o transforma una columna mediante una fórmula calculada | `df['nueva_col'] = expr` |
| `con` | Enlace para parámetros o fórmulas | `with` |
| `sanar` | Tratamiento y curación de valores nulos o faltantes | Limpieza de datos |
| `descartar_nulos` | Opción de sanación: elimina filas con valores nulos | `df.dropna()` |
| `llenar` | Opción de sanación: rellena nulos con un valor dado | `df[col].fillna(val)` |
| `destilar` / `agrupar` | Agrupa registros por una o varias columnas | `df.groupby(...)` |
| `agregar` / `resumir` | Aplica funciones de agregación estadística sobre grupos | `.agg(...)` |
| `como` | Asigna un alias o nombre a la columna agregada | `as` / alias |
| `preservar` / `guardar` | Exporta la poción de datos a un archivo CSV en disco | `df.to_csv(...)` |
| `en` | Especifica la ruta destino para exportar | `to` / `into` |
| `revelar` / `mostrar` | Imprime una muestra de la poción en consola | `print(df.head())` |
| `describir` | Genera o imprime estadísticas descriptivas de la poción | `df.describe()` |
| `forjar`, `artefacto` | Visualización gráfica (reconocida sintácticamente; Corte 3) | `matplotlib` |
| `y`, `o`, `no` | Operadores lógicos booleanos | `and`, `or`, `not` |
| `verdadero`, `falso` | Literales lógicos | `True`, `False` |

---

## 2. Funciones de Agregación Alquímica

Utilizadas dentro de la instrucción `destilar`:

| Función | Operación | Ejemplo |
|---|---|---|
| `suma(columna)` | Suma total de los valores del grupo | `suma(total) como ingreso` |
| `media(columna)` / `promedio` | Media aritmética | `media(precio) como precio_prom` |
| `mediana(columna)` | Mediana estadística | `mediana(edad) como edad_mediana` |
| `minimo(columna)` / `min` | Valor mínimo observado | `minimo(costo) como costo_min` |
| `maximo(columna)` / `max` | Valor máximo observado | `maximo(calificacion) como nota_max` |
| `desviacion(columna)` / `std` | Desviación estándar muestral | `desviacion(pm25) como dispersion` |
| `contar()` / `conteo` | Cantidad total de registros en el grupo | `contar() como total_pedidos` |

---

## 3. Operadores y Precedencia

| Categoría | Operadores | Comportamiento y Precedencia |
|---|---|---|
| Potencia | `^` | Mayor precedencia aritmética (`2 ^ 3 = 8`) |
| Multiplicativos | `*`, `/`, `%` | Multiplicación, división real y módulo |
| Aditivos | `+`, `-` | Suma (numérica o texto) y resta |
| Relacionales | `>`, `<`, `>=`, `<=`, `==`, `!=` | Comparaciones booleanas |
| Lógicos | `no` > `y` > `o` | Conectores lógicos de condiciones |
| Asignación | `=` | Almacena el resultado en una variable |

---

## 4. Estructura de las Sentencias Principales

### 1. Invocación (Carga de CSV)
```arc
ventas = invocar desde "csv/ventas.csv";
```

### 2. Inspección y Revelación
```arc
revelar ventas;
describir ventas;
```

### 3. Sanación (Datos Faltantes)
```arc
# Opción A: Descartar filas con nulos
ventas_limpias = sanar ventas descartar_nulos;

# Opción B: Rellenar nulos de una columna
ventas_rellenas = sanar ventas llenar descuento con 0.0;
```

### 4. Recolección (Selección de Columnas)
```arc
seleccion = recolectar [fecha, ciudad, total] de ventas;
```

### 5. Purificación (Filtrado de Filas)
```arc
filtradas = purificar ventas donde unidades > 0 y precio > 0;
```

### 6. Transmutación (Columnas Calculadas)
```arc
con_total = transmutar ventas con total = unidades * precio;
con_iva = transmutar con_total con total_iva = total * 1.19;
```

### 7. Ordenamiento
```arc
ordenadas = ordenar con_total por total desc;
```

### 8. Destilación (Agrupamiento y Agregación)
```arc
resumen = destilar ordenadas por [ciudad] agregar suma(total) como ingreso_total, media(total) como promedio_ticket, contar() como total_pedidos;
```

### 9. Preservación (Exportación a CSV)
```arc
preservar resumen en "salidas/resumen_ciudades.csv";
```
