# Datos didácticos: y = 2*x + 10. No representan mediciones reales.
modelo = regresion([1, 2, 3, 4], [12, 14, 16, 18]);
mostrar resumen_modelo(modelo);
mostrar predecir(modelo, 5); # 20
mostrar predecir_lote(modelo, [5, 6]); # [20, 22]
vecinos = knn([[1, 1], [2, 1], [8, 8], [9, 9]],
              ["bajo", "bajo", "alto", "alto"], 3);
mostrar predecir(vecinos, [1.5, 1.2]); # bajo
puntos = tabla(["x", "valor"], [[1, 1], [2, 1], [8, 8], [9, 9]]);
grupos = kmeans(puntos, ["x", "valor"], 2);
mostrar grupos;
red = mlp([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 1, 1, 0]);
mostrar predecir_lote(red, [[0, 0], [0, 1], [1, 0], [1, 1]]);
mostrar probabilidad(red, [0, 1]);
