# Compendio de matemáticas para Arcanum
# Librería propia del lenguaje construida desde cero sin usar import de Python

# Receta para calcular el impuesto sobre el valor agregado
receta calcular_iva(subtotal, tasa) {
    devolver subtotal * tasa;
}

# Receta para calcular el precio final aplicando un descuento
receta aplicar_descuento(precio, tasa_descuento) {
    monto_descuento = precio * tasa_descuento;
    devolver precio - monto_descuento;
}

# Receta para calcular la potencia de un número
receta potencia(base, exp) {
    devolver base ^ exp;
}

# Receta para generar un número aleatorio entre inicio y fin a partir de una semilla
receta azar(semilla, inicio, fin) {
    siguiente = (semilla * 1103515245 + 12345) % 2147483648;
    rango = (fin - inicio) + 1;
    devolver inicio + (siguiente % rango);
}

# Receta alias para calcular números random
receta random(semilla, inicio, fin) {
    devolver azar(semilla, inicio, fin);
}
