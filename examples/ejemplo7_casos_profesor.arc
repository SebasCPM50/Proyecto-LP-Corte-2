# Tres ejercicios: factorial, datos Excel y filtro de primos.
# 1. Multiplicar los enteros de 1 hasta n.
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


# 2. Leer una tabla, describirla y graficarla.
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


# 3. Conservar los numeros primos de una lista.
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
