# =============================================================================
# PROGRAMA COMPLETO 2: Analítica de Rendimiento Académico Universitario
# Dominio: Educación y Salud Académica
# Flujo: Carga -> Inspección -> Sanación -> Purificación ->
#        Transmutación -> Ordenamiento -> Destilación -> Preservación
# =============================================================================

# 1. Invocamos los registros académicos de los estudiantes
alumnos = invocar desde "csv/estudiantes.csv";

# 2. Revelamos las primeras filas de los datos
revelar alumnos;

# 3. Sanamos la poción descartando registros incompletos (con notas o datos faltantes)
alumnos_completos = sanar alumnos descartar_nulos;

# 4. Purificamos los datos conservando solo estudiantes con asistencia regular (>= 75%)
alumnos_regulares = purificar alumnos_completos donde asistencia >= 75;

# 5. Transmutamos la poción calculando la nota definitiva ponderada de ambos parciales
alumnos_evaluados = transmutar alumnos_regulares con nota_definitiva = (nota_parcial1 + nota_parcial2) / 2;

# 6. Ordenamos a los estudiantes de forma descendente según su nota definitiva obtenida
alumnos_ordenados = ordenar alumnos_evaluados por nota_definitiva desc;

# 7. Destilamos los resultados por carrera calculando métricas de rendimiento académico
resumen_academico = destilar alumnos_ordenados por [carrera] agregar media(nota_definitiva) como promedio_general, maximo(nota_definitiva) como nota_maxima, minimo(nota_definitiva) como nota_minima, media(asistencia) como asistencia_promedio, contar() como cantidad_alumnos;

# 8. Mostramos el resumen en consola y generamos estadísticas descriptivas
revelar resumen_academico;
describir resumen_academico;

# 9. Preservamos la tabla consolidada en el archivo de salida
preservar resumen_academico en "salidas/resumen_estudiantes.csv";
