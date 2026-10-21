# =============================================================================
# COMPENDIO: matematicas.arc
# Librería propia del lenguaje Arcanum construida desde cero
# No utiliza import de Python ni librerías externas.
# =============================================================================

# Receta para calcular el impuesto sobre el valor agregado
receta calcular_iva(subtotal, tasa) {
    devolver subtotal * tasa;
}

# Receta para calcular el precio final aplicando un descuento
receta aplicar_descuento(precio, tasa_descuento) {
    monto_descuento = precio * tasa_descuento;
    devolver precio - monto_descuento;
}

# Receta para calcular la potencia
receta potencia(base, exp) {
    devolver base ^ exp;
}
