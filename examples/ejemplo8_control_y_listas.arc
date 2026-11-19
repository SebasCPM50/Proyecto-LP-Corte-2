# Empezar aquí: variables, decisiones y repeticiones.
mostrar "Hola, Arcanum";
nota = 85;
si (nota >= 60) { mostrar "Aprobado"; }
sino { mostrar "Pendiente"; }
contador = 1;
acumulado = 0;
mientras (contador <= 5) {
    acumulado = acumulado + contador;
    contador = contador + 1;
}
mostrar acumulado; # 15
numeros = [10, 20, 30];
para numero en numeros { mostrar numero; }
mostrar numeros[0] + 5; # 15
mostrar rango(5, -1, -2); # [5, 3, 1]
