# =============================================================================
# COMPENDIO: estadistica.arc
# Librería propia del lenguaje Arcanum construida desde cero
# =============================================================================

# Receta para calcular el rango estadístico (diferencia entre max y min)
receta calcular_rango(maximo_val, minimo_val) {
    devolver maximo_val - minimo_val;
}

# Receta para calcular el porcentaje de una parte sobre un total
receta porcentaje(parte, total) {
    devolver (parte / total) * 100;
}
