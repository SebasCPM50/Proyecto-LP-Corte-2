# =============================================================================
# CASO DE ESTUDIO FINAL - CORTE 3 (PROYECTO ARCANUM)
# Flujo completo de Ciencia de Datos:
# Dominio: Aerolíneas y Vuelos Internacionales (Miami, Madrid, Cancún, Nueva York)
# Soporte Multiformato: Carga y exportación en CSV y JSON
# Carga -> Limpieza -> Transformación -> Matrices -> ML -> 4 Gráficas PNG -> Exportación
# =============================================================================

# 1. CARGA Y PREPARACIÓN DE DATOS (Pandas artesanal: Poción con CSV y JSON)
# Demostramos lectura multiformato nativa
vuelos_catalogo = invocar desde "datos/vuelos.json";
ventas_crudas = invocar desde "csv/ventas.csv";

ventas_sanas = sanar ventas_crudas llenar descuento con 0.0;
ventas_puras = purificar ventas_sanas donde unidades > 0 y precio > 0;
ventas_totales = transmutar ventas_puras con total = unidades * precio;
ventas_ordenadas = ordenar ventas_totales por total desc;

# 2. CONTROL DE FLUJO Y ESTRUCTURAS (Condicionales si/sino y Bucles mientras)
meta_ventas = 1000000;
ingreso_muestra = 1289500;

si (ingreso_muestra >= meta_ventas) {
    estado_meta = "Supero la meta de venta de pasajes";
} sino {
    estado_meta = "Por debajo de la meta de boletos";
}

# Simulación de ciclo con bucle mientras
paso = 1;
acumulador_ciclo = 0;
mientras (paso <= 5) {
    acumulador_ciclo = acumulador_ciclo + paso;
    paso = paso + 1;
}

# 3. ÁLGEBRA LINEAL Y MATRICES (NumPy artesanal)
matriz_a = matriz([[1, 2], [3, 4]]);
matriz_trans = transpuesta(matriz_a);

# 4. MACHINE LEARNING ARTESANAL
# A) Algoritmo de Predicción: Regresión Lineal (mínimos cuadrados)
historico_boletos = [1, 2, 3, 4, 5, 6];
historico_ingresos = [45000, 100000, 140000, 185000, 225000, 270000];
modelo_regresion = regresion(historico_boletos, historico_ingresos);
prediccion_7_boletos = predecir(modelo_regresion, 7);

# B) Algoritmo de Clasificación: K-Nearest Neighbors (KNN con distancia euclidiana)
datos_entrenamiento = [[1, 35000], [2, 45000], [4, 180000], [5, 220000]];
etiquetas_pasajeros = ["Frecuente", "Frecuente", "Corporativo", "Corporativo"];
modelo_knn = knn(datos_entrenamiento, etiquetas_pasajeros, 3);
clasificacion_nuevo_pasajero = predecir(modelo_knn, [3, 150000]);

# C) Algoritmo de Agrupamiento: K-Means (K-Medias clustering)
ventas_clusterizadas = kmeans(ventas_totales, ["unidades", "precio"], 3);

# 5. AGREGACIÓN ESTADÍSTICA (Destilación de datos por destino de vuelo)
resumen_ciudades = destilar ventas_totales por [ciudad] agregar
    suma(total) como ingreso_total,
    media(total) como ticket_promedio,
    contar() como total_transacciones;

revelar resumen_ciudades;

# 6. VISUALIZACIÓN MULTIMODAL (4 Gráficas exportadas a imágenes PNG)
# Gráfica 1: Barras
forjar artefacto barras desde resumen_ciudades con 
    eje_x ciudad, 
    eje_y ingreso_total, 
    titulo "1. Ingresos Totales por Destino de Vuelo", 
    salida "salidas/1_grafica_barras_ciudades.png";

# Gráfica 2: Líneas
forjar artefacto lineas desde ventas_ordenadas con 
    eje_x fecha, 
    eje_y total, 
    titulo "2. Evolución Temporal de Boletos Aéreos", 
    salida "salidas/2_grafica_lineas_ventas.png";

# Gráfica 3: Dispersión
forjar artefacto dispersion desde ventas_totales con 
    eje_x unidades, 
    eje_y total, 
    titulo "3. Pasajeros vs Ingreso por Venta", 
    salida "salidas/3_grafica_dispersion.png";

# Gráfica 4: Histograma
forjar artefacto histograma desde ventas_totales con 
    eje_x total, 
    titulo "4. Distribución de Tarifas de Boletos", 
    salida "salidas/4_grafica_histograma_precios.png";

# 7. PRESERVACIÓN DEL RESULTADO EN MÚLTIPLES FORMATOS (CSV y JSON)
preservar resumen_ciudades en "salidas/resumen_caso_estudio_final.csv";
preservar resumen_ciudades en "salidas/resumen_caso_estudio_final.json";
