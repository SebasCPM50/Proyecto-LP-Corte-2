# =============================================================================
# PUNTO 4: Análisis Exploratorio de Datos (EDA)
# =============================================================================

# 1. Cargar el Excel
censo = invocar desde "datos/data.xlsx";

# 2. Resumen estadístico automático (media, desv, min, max)
describir censo;

# 3. Agrupación por nivel educativo
resumen = destilar censo por [nivel_edu] agregar
    contar() como total_personas,
    media(ingreso_mensual) como ingreso_promedio;
revelar resumen;

# 4. Gráfica de barras
graficar barras desde resumen con
    eje_x nivel_edu,
    eje_y ingreso_promedio,
    titulo "Ingreso Promedio por Nivel Educativo",
    salida "salidas/eda_educacion.png";

# 5. Exportar a CSV
preservar resumen en "salidas/resumen_eda.csv";
