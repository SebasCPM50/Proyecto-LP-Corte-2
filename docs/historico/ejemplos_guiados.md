# EJEMPLOS GUIADOS PASO A PASO — ARCANUM

En esta guía encontrarás 4 tutoriales prácticos completos con datos reales, mostrando el código fuente y lo que produce cada paso del análisis.

---

## CASO 1: ANÁLISIS DE VENTAS COMERCIALES

* **Archivo de entrada:** `csv/ventas.csv`
* **Script ejecutable:** `examples/ejemplo1_analisis_ventas.arc`
* **Objetivo:** Limpiar ventas con descuentos nulos, filtrar compras reales, calcular el total por transacción, ordenar de mayor a menor y resumir las ventas por ciudad.

### Código del Grimorio
```arc
# 1. Cargar el dataset de ventas
ventas_crudas = invocar desde "csv/ventas.csv";
revelar ventas_crudas;

# 2. Curar valores nulos: si el descuento es nulo, le asignamos 0.0
ventas_rellenas = sanar ventas_crudas llenar descuento con 0.0;

# 3. Seleccionar las columnas que nos interesan
ventas_reducidas = recolectar [fecha, ciudad, categoria, unidades, precio_unitario, precio, descuento] de ventas_rellenas;

# 4. Filtrar registros inválidos: solo compras con unidades mayores o iguales a 1
ventas_validas = purificar ventas_reducidas donde (unidades >= 1);

# 5. Crear columnas calculadas: subtotal y total final
ventas_subtotal = transmutar ventas_validas con subtotal = unidades * precio_unitario;
ventas_totales = transmutar ventas_subtotal con total = subtotal - (subtotal * descuento);

# 6. Ordenar de mayor a menor por el total
ventas_ordenadas = ordenar ventas_totales por total desc;

# 7. Resumir por ciudad calculando total facturado, ticket promedio y número de transacciones
resumen_ciudades = destilar ventas_ordenadas agrupar [ciudad] agregando [
    suma total como ingreso_total,
    media total como ticket_promedio,
    contar como total_transacciones
];

# 8. Visualizar resultados y exportar
revelar resumen_ciudades;
describir resumen_ciudades;
preservar resumen_ciudades en "salidas/resumen_ventas_ciudad.csv";
```

### Cómo ejecutar este caso
```bash
python3 src/main.py examples/ejemplo1_analisis_ventas.arc
```

---

## CASO 2: RENDIMIENTO ACADÉMICO ESTUDIANTIL

* **Archivo de entrada:** `csv/estudiantes.csv`
* **Script ejecutable:** `examples/ejemplo2_rendimiento_estudiantil.arc`
* **Objetivo:** Manejar notas no presentadas asignando 0.0, calcular si el estudiante aprobó, y resumir el promedio de calificaciones por carrera.

### Código del Grimorio
```arc
# 1. Cargar las notas estudiantiles
estudiantes = invocar desde "csv/estudiantes.csv";

# 2. Imputar nota 0.0 a quienes no presentaron
estudiantes_sanos = sanar estudiantes llenar calificacion con 0.0;

# 3. Filtrar estudiantes activos con asistencia suficiente
estudiantes_activos = purificar estudiantes_sanos donde (asistencia >= 70);

# 4. Ordenar por calificación de mayor a menor
estudiantes_ordenados = ordenar estudiantes_activos por calificacion desc;

# 5. Resumir métricas por carrera académica
resumen_carreras = destilar estudiantes_ordenados agrupar [carrera] agregando [
    media calificacion como promedio_carrera,
    desviacion calificacion como dispersion_notas,
    contar como cantidad_alumnos
];

revelar resumen_carreras;
preservar resumen_carreras en "salidas/resumen_estudiantes.csv";
```

### Cómo ejecutar este caso
```bash
python3 src/main.py examples/ejemplo2_rendimiento_estudiantil.arc
```

---

## CASO 3: MONITOREO DE CALIDAD DEL AIRE Y AMBIENTAL

* **Archivo de entrada:** `csv/calidad_aire.csv`
* **Script ejecutable:** `examples/ejemplo3_calidad_aire.arc`
* **Objetivo:** Descartar registros con sensores dañados, filtrar temperaturas representativas y resumir la concentración de material particulado PM2.5 por estación.

### Código del Grimorio
```arc
# 1. Cargar mediciones ambientales
aire = invocar desde "csv/calidad_aire.csv";

# 2. Descartar sensores que reportaron nulo
aire_limpio = sanar aire descartar_nulos;

# 3. Filtrar mediciones en rango diurno con temperatura mayor a 18 grados
aire_filtrado = purificar aire_limpio donde (temperatura > 18.0);

# 4. Resumir la contaminación PM2.5 por estación de monitoreo
resumen_estaciones = destilar aire_filtrado agrupar [estacion] agregando [
    media pm25 como pm25_promedio,
    desviacion pm25 como variabilidad_pm25,
    maximo pm25 como pico_maximo,
    contar como mediciones_totales
];

revelar resumen_estaciones;
describir resumen_estaciones;
preservar resumen_estaciones en "salidas/resumen_calidad_aire.csv";
```

### Cómo ejecutar este caso
```bash
python3 src/main.py examples/ejemplo3_calidad_aire.arc
```

---

## CASO 4: USO DE COMPENDIOS Y RECETAS MODULARES

* **Archivo ejecutable:** `examples/ejemplo4_compendios_recetas.arc`
* **Objetivo:** Mostrar cómo importar y reutilizar funciones de la librería matemática de Arcanum y generar números de azar sin usar librerías externas.

### Código del Grimorio
```arc
# 1. Cargar el compendio matemático propio de Arcanum
usar compendio matematicas;

# 2. Definir variables y aplicar funciones del compendio
subtotal = 350000;
iva = matematicas.calcular_iva(subtotal, 0.19);
total = subtotal + iva;

# 3. Usar la función aleatoria integrada
sorteo = random(1, 100);

# 4. Definir una receta propia en el mismo archivo
receta bonificacion(monto) {
    si_aplica = monto * 0.05;
    devolver si_aplica;
}

bono = bonificacion(total);

revelar total;
revelar bono;
```

### Cómo ejecutar este caso
```bash
python3 src/main.py examples/ejemplo4_compendios_recetas.arc
```
