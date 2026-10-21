# PROGRAMA COMPLETO 1: Análisis de Ventas y Rendimiento Comercial
# Dominio: Comercio y Finanzas
# Flujo: Carga -> Inspección -> Sanación -> Selección -> Purificación -> Transmutación -> Ordenamiento -> Destilación -> Preservación

# 1 Invocamos la poción con los datos crudos de ventas
ventas_crudas = invocar desde "csv/ventas.csv";

# 2 Revelamos las filas en consola para inspección inicial
revelar ventas_crudas;

# 3 Sanamos los valores nulos en el descuento rellenándolos con 0.0
ventas_rellenas = sanar ventas_crudas llenar descuento con 0.0;

# 4 Recolectamos únicamente los ingredientes que nos interesan
ventas_reducidas = recolectar [fecha, ciudad, categoria, unidades, precio_unitario, precio, descuento] de ventas_rellenas;

# 5 Purificamos las filas descartando registros con unidades o precios inválidos
ventas_validas = purificar ventas_reducidas donde unidades > 0 y precio > 0;

# 6 Transmutamos la poción calculando el subtotal y luego el total final con descuento
ventas_subtotal = transmutar ventas_validas con subtotal = unidades * precio;
ventas_totales = transmutar ventas_subtotal con total = subtotal - (subtotal * descuento);

# 7 Ordenamos las ventas de mayor a menor según el ingreso generado
ventas_ordenadas = ordenar ventas_totales por total desc;

# 8 Destilamos la poción agrupando por ciudad para obtener métricas agregadas
resumen_ciudades = destilar ventas_ordenadas por [ciudad] agregar suma(total) como ingreso_total, media(total) como ticket_promedio, contar() como total_transacciones;

# 9 Revelamos el resumen obtenido en consola y mostramos sus estadísticas
revelar resumen_ciudades;
describir resumen_ciudades;

# 10 Preservamos la tabla final en un archivo CSV exportado
preservar resumen_ciudades en "salidas/resumen_ventas_ciudad.csv";
