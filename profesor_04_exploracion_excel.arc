# =============================================================================
# PUNTO 4: Análisis Exploratorio de Datos (EDA) desde Excel (Data.xlsx)
# Dataset: Censo Socioeconómico (10,280 registros)
# Columnas: id, edad, nivel_edu, ingreso_mensual, sex, anios_esc
# =============================================================================

mostrar "=== 1. CARGA DE DATOS DESDE EXCEL ===";
censo = invocar desde "datos/Data.xlsx";
mostrar "Total de registros cargados: " + longitud(censo);

mostrar "";
mostrar "=== 2. ESTADÍSTICAS DESCRIPTIVAS (VARIABLES NUMÉRICAS) ===";
# Seleccionamos las variables cuantitativas para el análisis estadístico
metricas = recolectar [edad, ingreso_mensual, anios_esc] de censo;
resumen_stats = describir metricas;
mostrar resumen_stats;
preservar resumen_stats en "salidas/eda_estadisticas_censo.csv";

mostrar "";
mostrar "=== 3. ANÁLISIS POR NIVEL EDUCATIVO ===";
por_educacion = destilar censo por [nivel_edu] agregar
    contar() como personas,
    media(ingreso_mensual) como ingreso_medio,
    media(anios_esc) como escolaridad_media;
mostrar por_educacion;
preservar por_educacion en "salidas/eda_por_educacion.csv";

mostrar "";
mostrar "=== 4. ANÁLISIS POR SEXO ===";
por_sexo = destilar censo por [sex] agregar
    contar() como personas,
    media(ingreso_mensual) como ingreso_medio,
    media(edad) como edad_media;
mostrar por_sexo;
preservar por_sexo en "salidas/eda_por_sexo.csv";

mostrar "";
mostrar "=== 5. GENERACIÓN DE ARTEFACTOS VISUALES (GRÁFICAS) ===";

# Gráfica 1: Barras de Ingreso Medio por Nivel Educativo
graficar barras desde por_educacion con
    eje_x nivel_edu,
    eje_y ingreso_medio,
    titulo "Ingreso Medio por Nivel Educativo",
    salida "salidas/eda_ingreso_educacion.png";

# Gráfica 2: Barras de Distribución por Sexo
graficar barras desde por_sexo con
    eje_x sex,
    eje_y personas,
    titulo "Distribucion de Personas por Sexo",
    salida "salidas/eda_poblacion_sexo.png";

# Gráfica 3: Histograma de Distribución de Edad
graficar histograma desde censo con
    eje_x edad,
    titulo "Distribucion de Edades de la Poblacion",
    salida "salidas/eda_distribucion_edad.png";

# Gráfica 4: Dispersión entre Años de Escolaridad e Ingreso Mensual
graficar dispersion desde censo con
    eje_x anios_esc,
    eje_y ingreso_mensual,
    titulo "Escolaridad vs Ingreso Mensual",
    salida "salidas/eda_escolaridad_ingreso.png";

mostrar "";
mostrar "=== ANÁLISIS EXPLORATORIO COMPLETADO EXITOSAMENTE ===";
