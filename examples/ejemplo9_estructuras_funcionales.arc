receta doble(n) { devolver n * 2; }
receta es_par(n) {
    si (n % 2 == 0) { devolver verdadero; }
    devolver falso;
}
receta acumular(a, b) { devolver a + b; }
numeros = [1, 2, 3, 4, 5];
dobles = mapear(numeros, "doble");
pares = filtrar(numeros, "es_par");
total = reducir(numeros, "acumular", 0);
mostrar numeros; # El original sigue igual.
mostrar dobles; # [2, 4, 6, 8, 10]
mostrar pares; # [2, 4]
mostrar total; # 15
A = matriz([[1, 2], [3, 4]]);
B = matriz([[2, 0], [1, 2]]);
mostrar multiplicar_matrices(A, B); # [[4, 4], [10, 8]]
mostrar transpuesta(A);
mostrar A[1][0]; # 3
