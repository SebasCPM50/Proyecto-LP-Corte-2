# =============================================================================
# PUNTO 1: Factorial de una lista de números [5 - 100]
# El rendimiento se mide externamente desde Python con medir_punto1.py
# =============================================================================

receta factorial(n) {
    resultado = 1;
    contador = 1;
    mientras (contador <= n) {
        resultado = resultado * contador;
        contador = contador + 1;
    }
    devolver resultado;
}

# Lista del 5 al 100 (según el enunciado del tablero)
numeros = rango(5, 101);

# Aplicamos la función de orden superior 'mapear'
factoriales = mapear(numeros, "factorial");

# Revelamos el resultado
revelar factoriales;
