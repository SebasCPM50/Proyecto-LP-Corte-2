# CATÁLOGO DE INSTRUCCIONES — ARCANUM

## PALABRAS CLAVE Y OPERADORES

| Palabra clave | Significado alquímico | Equivalente en Ciencia de Datos |
| :--- | :--- | :--- |
| `invocar` | Carga un archivo CSV a memoria | `pd.read_csv(...)` |
| `desde` | Indica la ruta del archivo CSV | Origen de datos |
| `recolectar` | Selecciona un grupo de columnas | `df[['col1', 'col2']]` |
| `de` | Indica la poción sobre la que se seleccionan columnas | Fuente tabular |
| `purificar` | Filtra registros según una condición lógica | `df[condicion]` |
| `donde` | Introduce la condición booleana | Cláusula `where` |
| `ordenar` | Ordena las filas según una columna | `df.sort_values(...)` |
| `por` | Indica la columna de ordenamiento | Criterio de orden |
| `asc` / `ascendente` | Orden de menor a mayor | `ascending=True` |
| `desc` / `descendente` | Orden de mayor a menor | `ascending=False` |
| `transmutar` | Agrega una columna calculada | `df['nueva_col'] = formula` |
| `con` | Enlace para definir la fórmula calculada | Asignación de cálculo |
| `sanar` | Tratamiento y curación de celdas vacías o nulas | Limpieza de datos |
| `descartar_nulos` | Elimina filas que contengan al menos un nulo | `df.dropna()` |
| `llenar` | Rellena celdas nulas con un valor por defecto | `df['col'].fillna(val)` |
| `destilar` / `agrupar` | Agrupa filas por categorías | `df.groupby(...)` |
| `agregando` | Introduce la lista de funciones agregadas | `.agg(...)` |
| `como` | Asigna un alias a la columna calculada | Alias de salida |
| `describir` | Muestra resumen con media, desviación, min y max | `df.describe()` |
| `revelar` | Imprime la tabla completa en consola | `print(df)` |
| `preservar` | Exporta la tabla a un archivo CSV en disco | `df.to_csv(...)` |
| `en` | Indica la ruta del archivo de salida | Destino de exportación |
| `random` / `azar` | Genera números aleatorios o muestrea filas | Generador pseudoaleatorio |
| `usar` `compendio` | Carga una librería propia escrita en Arcanum | Importación propia |
| `receta` | Define una función reutilizable | `def funcion(...)` |
| `devolver` | Retorna el resultado de una receta | `return` |
| `y`, `o`, `no` | Operadores lógicos | `and`, `or`, `not` |
| `verdadero`, `falso` | Valores booleanos | `True`, `False` |

---

## OPERACIONES DE CIENCIA DE DATOS

### Invocación de archivos (Carga de datos)
Carga un archivo CSV desde disco a una Poción en memoria sin librerías externas:
```arc
datos = invocar desde "csv/ventas.csv";
```

### Recolección (Selección de columnas)
Conserva únicamente las columnas indicadas y descarta las demás:
```arc
seleccion = recolectar [fecha, ciudad, total] de datos;
```

### Purificación (Filtrado de filas)
Conserva solo los registros que cumplan la condición matemática o lógica:
```arc
filtradas = purificar datos donde (unidades >= 2 y precio > 50000);
```

### Ordenamiento (Ordenar registros)
Ordena las filas de forma ascendente o descendente manejando valores nulos de forma segura:
```arc
ordenadas_asc = ordenar datos por precio asc;
ordenadas_desc = ordenar datos por total desc;
```

### Transmutación (Columnas calculadas)
Calcula una nueva columna fila por fila aplicando operadores aritméticos:
```arc
con_subtotal = transmutar datos con subtotal = unidades * precio_unitario;
```

### Sanación (Limpieza de nulos)
Elimina registros incompletos o imputa valores por defecto:
```arc
# Opción 1: Descartar cualquier fila con valores nulos
limpias = sanar datos descartar_nulos;

# Opción 2: Rellenar nulos de una columna específica
rellenas = sanar datos llenar descuento con 0.0;
```

### Destilación (Agrupación y agregación)
Agrupa registros por una o más categorías y calcula estadísticas sobre el grupo:
```arc
resumen = destilar datos agrupar [ciudad] agregando [
    suma unidades como total_unidades,
    media precio_unitario como precio_promedio,
    contar como total_ventas
];
```

### Descripción estadística
Calcula y muestra conteo, media, desviación estándar, mínimo y máximo de todas las columnas numéricas:
```arc
describir datos;
```

### Revelación (Visualización en consola)
Imprime en pantalla la tabla con alineación dinámica y mostrando explícitamente los valores `None`:
```arc
revelar datos;
```

### Preservación (Exportación a CSV)
Guarda la poción en un archivo CSV en disco:
```arc
preservar datos en "salidas/resultado.csv";
```

---

## FUNCIONES DE AGREGACIÓN ESTADÍSTICA

Utilizadas dentro de la instrucción `destilar`:

| Función | Operación matemática realizada | Ejemplo de uso |
| :--- | :--- | :--- |
| `suma` | Suma de los valores numéricos del grupo | `suma precio como total_precio` |
| `media` / `promedio` | Promedio aritmético muestral $\frac{\sum x}{n}$ | `media calificacion como promedio_nota` |
| `mediana` | Valor central del conjunto ordenado | `mediana salario como salario_mediano` |
| `desviacion` / `std` | Desviación estándar muestral $\sqrt{\frac{\sum (x - \bar{x})^2}{n - 1}}$ | `desviacion pm25 como dispersion` |
| `minimo` / `min` | Valor mínimo registrado en el grupo | `minimo edad como edad_minima` |
| `maximo` / `max` | Valor máximo registrado en el grupo | `maximo ingreso como ingreso_maximo` |
| `contar` / `conteo` | Cantidad total de filas del grupo | `contar como cantidad_transacciones` |

---

## FUNCIONES DE AZAR Y MATEMÁTICAS

### Función random integrada
Genera números pseudoaleatorios mediante un algoritmo congruencial lineal hecho desde cero:
```arc
# Retorna un decimal al azar entre 0.0 y 1.0
probabilidad = random();

# Retorna un número entero al azar entre 0 y 100
porcentaje = random(100);

# Retorna un número entero al azar entre 1 y 6 (dado)
tirada = random(1, 6);
```

### Recetas de compendios matemáticos
Cargando la librería de matemáticas con `usar compendio matematicas;`:
```arc
usar compendio matematicas;

# Cálculo de IVA
iva = matematicas.calcular_iva(150000, 0.19);

# Aplicar descuento
precio_final = matematicas.aplicar_descuento(200000, 0.10);

# Potenciación
resultado = matematicas.potencia(2, 8);

# Número pseudoaleatorio con semilla
azar = matematicas.random(42, 10, 50);
```

---

## DEFINICIÓN DE RECETAS (FUNCIONES PROPIAS)

Permite crear subrutinas reutilizables con paso de parámetros y memoria local:
```arc
receta calcular_ganancia(costo, venta) {
    margen = venta - costo;
    devolver margen;
}

utilidad = calcular_ganancia(80000, 120000);
```
