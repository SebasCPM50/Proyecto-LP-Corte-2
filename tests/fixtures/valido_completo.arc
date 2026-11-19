descuento = 0.10;
umbral = 100 * descuento;
activo = verdadero;

ventas = invocar desde "datos/ventas.csv";
ventas_reducidas = recolectar [fecha, ciudad, categoria, unidades, precio] de ventas;
ventas_validas = purificar ventas_reducidas donde unidades > 0 y precio > 0;

forjar artefacto barras desde ventas_validas con eje_x ciudad, eje_y precio, titulo "Precios por ciudad";
