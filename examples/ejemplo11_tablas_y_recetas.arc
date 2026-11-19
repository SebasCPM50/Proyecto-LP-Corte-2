# Crear una tabla sin archivos externos y procesarla en una receta.
receta preparar(origen) {
    seleccion = purificar origen donde cantidad >= 2;
    calculada = transmutar seleccion con total = cantidad * precio;
    mostrar calculada;
    devolver calculada;
}
ventas = tabla(["producto", "cantidad", "precio"],
               [["Libro", 2, 10], ["Lapiz", 1, 2], ["Libro", 3, 10]]);
resultado = preparar(ventas);
resumen = destilar resultado por [producto] agregar suma(total) como ingreso;
mostrar resumen; # Libro: 50
valores = columna(resultado, "total");
mostrar valores; # [20, 30]
M = a_matriz(resultado, ["cantidad", "precio"]);
mostrar M;
preservar resumen en "salidas/ejemplo11_resumen.csv";
