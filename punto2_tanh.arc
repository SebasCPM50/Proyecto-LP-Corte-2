# =============================================================================
# PUNTO 2: Visualizar Tangente Hiperbólica tanh(x)
# =============================================================================

filas = [];

# Evaluamos x en el rango de -5 a 5
para x en rango(-5, 6) {
    valor = tanh(x);
    filas = anexar(filas, [x, valor]);
}

# Creamos la tabla de datos (x, tanh_x)
datos = tabla(["x", "tanh_x"], filas);
revelar datos;

# Generamos la gráfica de líneas en PNG
graficar lineas desde datos con
    eje_x x,
    eje_y tanh_x,
    titulo "Funcion Tangente Hiperbolica tanh(x)",
    salida "salidas/grafica_tanh.png";

mostrar "=== GRÁFICA GENERADA EN salidas/grafica_tanh.png ===";
