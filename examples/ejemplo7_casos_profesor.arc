# =============================================================================
# PROGRAMA COMPLETO 7: RESOLUCIÓN DE LOS 5 CASOS DE EVALUACIÓN
# Basado exactamente en los ejercicios solicitados por el docente en tablero:
# (1) Función que calcule el factorial # 5-100
# (2) Visualizar la función Sigmoide S(x)
# (3) Analizar el perceptrón multicapa para XOR [Gráficas, Estimador]
# (4) Data.xlsx -> Realizar un Análisis Exploratorio de datos (EDA)
# (5) Implementar funcionalmente filtro para datos que sean de tipo primo
# =============================================================================

# -----------------------------------------------------------------------------
# EJERCICIO 1: Función que calcula el factorial (# 5-100)
# -----------------------------------------------------------------------------
receta factorial(n) {
    resultado = 1;
    contador = 1;
    mientras (contador <= n) {
        resultado = resultado * contador;
        contador = contador + 1;
    }
    devolver resultado;
}

fact_5 = factorial(5);
fact_10 = factorial(10);
revelar fact_5;
revelar fact_10;
fact_100 = factorial(100);
revelar fact_100;

# -----------------------------------------------------------------------------
# EJERCICIO 2: Visualizar la función Sigmoide S(x) = 1 / (1 + e^(-x))
# -----------------------------------------------------------------------------
# Calculamos puntos de la curva sigmoide en el intervalo [-6, 6]
sig_neg4 = sigmoide(0 - 4);
sig_cero = sigmoide(0);
sig_pos4 = sigmoide(4);

revelar sig_cero;

# Construimos los puntos reales de la función sigmoide.
puntos_sigmoide = [];
para x en rango(-6, 7) {
    puntos_sigmoide = anexar(puntos_sigmoide, [x, sigmoide(x)]);
}
curva_sigmoide = tabla(["x", "probabilidad"], puntos_sigmoide);
graficar lineas desde curva_sigmoide con eje_x x, eje_y probabilidad,
    titulo "Funcion sigmoide", salida "salidas/6_grafica_sigmoide_tendencia.png";
preservar curva_sigmoide en "salidas/sigmoide.csv";

# -----------------------------------------------------------------------------
# EJERCICIO 3: Analizar el Perceptrón Multicapa para XOR [Gráficas, Estimador]
# -----------------------------------------------------------------------------
# Tabla de verdad del operador no lineal XOR:
# [0, 0] -> 0
# [0, 1] -> 1
# [1, 0] -> 1
# [1, 1] -> 0
X_xor = [[0, 0], [0, 1], [1, 0], [1, 1]];
y_xor = [0, 1, 1, 0];

# Estimador de Red Neuronal Artificial (MLP)
modelo_xor = mlp(X_xor, y_xor);

# Evaluamos las 4 combinaciones posibles con el estimador entrenado
pred_0_0 = predecir(modelo_xor, [0, 0]);
pred_0_1 = predecir(modelo_xor, [0, 1]);
pred_1_0 = predecir(modelo_xor, [1, 0]);
pred_1_1 = predecir(modelo_xor, [1, 1]);

revelar pred_0_0;
revelar pred_0_1;
revelar pred_1_0;
revelar pred_1_1;
perdidas_xor = historial(modelo_xor);
graficar lineas desde perdidas_xor con eje_x epoca, eje_y perdida,
    titulo "Aprendizaje de XOR", salida "salidas/8_perdida_xor.png";
preservar perdidas_xor en "salidas/perdida_xor.csv";

# -----------------------------------------------------------------------------
# EJERCICIO 4: Data.xlsx -> Realizar un Análisis Exploratorio de datos (EDA)
# -----------------------------------------------------------------------------
# Invocamos la hoja de cálculo Excel directamente sin intermediarios
datos_excel = invocar desde "datos/Data.xlsx";

# Revelación tabular y resumen exploratorio (conteo, media, std, min, max)
revelar datos_excel;
describir datos_excel;

# Gráfica exploratoria para el EDA (distribución de pasajeros por aerolínea)
forjar artefacto barras desde datos_excel con
    eje_x aerolinea,
    eje_y pasajeros,
    titulo "EDA: Pasajeros por Aerolinea desde Data.xlsx",
    salida "salidas/7_eda_pasajeros_excel.png";

# -----------------------------------------------------------------------------
# EJERCICIO 5: Implementar funcionalmente filtro para datos de tipo primo
# -----------------------------------------------------------------------------
receta es_primo(numero) {
    resultado_primo = 1;
    si (numero <= 1) {
        resultado_primo = 0;
    }
    divisor = 2;
    mientras (divisor * divisor <= numero) {
        si (numero % divisor == 0) {
            resultado_primo = 0;
        }
        divisor = divisor + 1;
    }
    devolver resultado_primo;
}

# Verificamos números primos
es_primo_2 = es_primo(2);
es_primo_7 = es_primo(7);
es_primo_9 = es_primo(9);
es_primo_13 = es_primo(13);

revelar es_primo_2;
revelar es_primo_7;
revelar es_primo_9;
revelar es_primo_13;

# Filtro funcional sobre la colección completa.
primos = filtrar(rango(2, 31), "es_primo");
revelar primos;
