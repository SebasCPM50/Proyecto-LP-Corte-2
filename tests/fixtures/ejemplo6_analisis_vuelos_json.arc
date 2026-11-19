# =============================================================================
# PROGRAMA COMPLETO 6: Analítica de Vuelos Comerciales y Retrasos
# Dominio: Aviación Comercial y Transporte Aéreo
# Formato: Invocación y Preservación en formato JSON nativo
# =============================================================================

# 1. Invocamos los registros de vuelos directamente desde un archivo JSON
vuelos = invocar desde "datos/vuelos.json";

revelar vuelos;

# 2. Purificamos los vuelos que tuvieron algún retraso (retraso mayor a 0 minutos)
vuelos_retrasados = purificar vuelos donde retraso_min > 0;

# 3. Ordenamos de mayor a menor según los minutos de retraso
vuelos_ordenados = ordenar vuelos_retrasados por retraso_min desc;

revelar vuelos_ordenados;

# 4. Destilamos agrupando por aerolínea para calcular métricas de puntualidad
resumen_retrasos = destilar vuelos_retrasados por [aerolinea] agregar
    suma(retraso_min) como minutos_totales,
    media(retraso_min) como promedio_retraso,
    contar() como total_vuelos_afectados;

revelar resumen_retrasos;
describir resumen_retrasos;

# 5. Forjamos una gráfica de barras comparando el promedio de retraso por aerolínea
forjar artefacto barras desde resumen_retrasos con
    eje_x aerolinea,
    eje_y promedio_retraso,
    titulo "Minutos de Retraso Promedio por Aerolinea",
    salida "salidas/5_grafica_retraso_aerolineas.png";

# 6. Preservamos el resultado directamente en formato JSON
preservar resumen_retrasos en "salidas/resumen_retrasos_aerolineas.json";
