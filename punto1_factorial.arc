# =============================================================================
# PUNTO 1: Factorial de una lista de números [1 - n]
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

# Lista de números del 1 al 10 (puedes cambiar 11 por cualquier n + 1)
numeros = rango(1, 11);

# Aplicamos la función de orden superior 'mapear'
factoriales = mapear(numeros, "factorial");

# Revelamos la lista resultante de factoriales
revelar factoriales;
