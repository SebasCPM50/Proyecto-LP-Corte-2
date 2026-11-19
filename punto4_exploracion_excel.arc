# =============================================================================
# PUNTO 4: Análisis Exploratorio de Datos (EDA) desde Excel (.xlsx)
# =============================================================================

# 1. Invocamos directamente la hoja de cálculo de Excel
datos_excel = invocar desde "datos/Data.xlsx";

# 2. Revelamos las filas para inspección inicial
revelar datos_excel;

# 3. Análisis exploratorio automático (conteo, media, desviación, min, max)
describir datos_excel;

# 4. Agrupamos por aerolínea para analizar métricas por categoría
resumen_aerolineas = destilar datos_excel por [aerolinea] agregar
    contar() como total_vuelos,
    media(pasajeros) como promedio_pasajeros,
    media(precio) como precio_promedio;

revelar resumen_aerolineas;

# 5. Generamos una gráfica exploratoria de barras en PNG
forjar artefacto barras desde resumen_aerolineas con
    eje_x aerolinea,
    eje_y promedio_pasajeros,
    titulo "EDA: Pasajeros Promedio por Aerolinea",
    salida "salidas/eda_pasajeros_excel.png";

# 6. Preservamos el resultado en CSV
preservar resumen_aerolineas en "salidas/resumen_eda_excel.csv";
