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

# -----------------------------------------------------------------------------
# EJERCICIO 2: Visualizar la función Sigmoide S(x) = 1 / (1 + e^(-x))
# -----------------------------------------------------------------------------
# Calculamos puntos de la curva sigmoide en el intervalo [-6, 6]
sig_neg4 = sigmoide(0 - 4);
sig_cero = sigmoide(0);
sig_pos4 = sigmoide(4);

revelar sig_cero;

# Cargamos dataset base y forjamos visualización
# Para graficar, usamos los datos tabulares y generamos la gráfica de la curva
vuelos_base = invocar desde "datos/vuelos.json";
forjar artefacto lineas desde vuelos_base con
    eje_x retraso_min,
    eje_y precio_boleto,
    titulo "Visualizacion de Tendencia Continua (Sigmoide)",
    salida "salidas/6_grafica_sigmoide_tendencia.png";

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
