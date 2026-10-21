# =============================================================================
# PROGRAMA COMPLETO 3: Monitoreo Ambiental de Calidad del Aire
# Dominio: Ciencias Ambientales y Sensores Urbanos
# Flujo: Carga -> Inspección -> Sanación -> Purificación ->
#        Transmutación -> Ordenamiento -> Destilación -> Preservación
# =============================================================================

# 1. Invocamos las lecturas registradas por las estaciones meteorológicas
lecturas = invocar desde "csv/calidad_aire.csv";

# 2. Revelamos las primeras filas en consola para verificar los datos
revelar lecturas;

# 3. Sanamos la poción rellenando los valores faltantes de PM10 con la media estimada (50.0)
lecturas_sanadas = sanar lecturas llenar pm10 con 50.0;

# 4. Purificamos los datos descartando anomalías físicas (mediciones negativas o erróneas del sensor)
lecturas_validas = purificar lecturas_sanadas donde pm25 > 0 y pm10 > 0 y temperatura > 0;

# 5. Transmutamos la poción calculando el porcentaje de partículas finas (PM2.5 / PM10)
lecturas_indice = transmutar lecturas_validas con razon_pm = (pm25 / pm10) * 100;

# 6. Ordenamos las lecturas por la razón de partículas de mayor a menor criticidad
lecturas_ordenadas = ordenar lecturas_indice por razon_pm desc;

# 7. Destilamos los registros por estación meteorológica calculando promedios y máximos
resumen_ambiental = destilar lecturas_ordenadas por [estacion] agregar media(pm25) como pm25_promedio, maximo(pm25) como pm25_maximo, media(pm10) como pm10_promedio, media(razon_pm) como razon_pm_promedio, media(temperatura) como temperatura_promedio, contar() como muestras_totales;

# 8. Revelamos el reporte ambiental y generamos estadísticas descriptivas
revelar resumen_ambiental;
describir resumen_ambiental;

# 9. Preservamos la tabla final en un archivo CSV para las autoridades ambientales
preservar resumen_ambiental en "salidas/resumen_calidad_aire.csv";
