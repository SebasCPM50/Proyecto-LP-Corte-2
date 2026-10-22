# PROGRAMA COMPLETO 4: Demostración de Librerías Propias (Compendios y Recetas)

# 1 Cargamos el compendio propio de matemáticas
usar compendio matematicas;

# 2 Definimos una receta local propia para calcular comisión
receta comision_vendedor(monto, tasa) {
    comision = monto * tasa;
    devolver comision;
}

# 3 Probamos las funciones de la librería propia
subtotal_ejemplo = 100000;
iva = matematicas.calcular_iva(subtotal_ejemplo, 0.19);
precio_rebajado = matematicas.aplicar_descuento(subtotal_ejemplo, 0.15);
mi_comision = comision_vendedor(subtotal_ejemplo, 0.05);

# 4 Invocamos datos y usamos operaciones alquímicas
ventas = invocar desde "csv/ventas.csv";
ventas_puras = purificar ventas donde unidades > 0 y precio > 0;
ventas_con_iva = transmutar ventas_puras con precio_final = precio * 1.19;

revelar ventas_con_iva;
preservar ventas_con_iva en "salidas/ventas_con_librerias_propias.csv";
