"""
Módulo de Arreglo Funcional para Arcanum
Representa secuencias ordenadas de datos con operaciones del paradigma funcional
(map, filter, reduce) e inmutabilidad, sin usar librerías externas.
"""


class Arreglo:
    """
    Estructura de datos artesanal de 1 dimensión para Arcanum.
    Diseñada bajo el paradigma funcional: cada transformación retorna un nuevo Arreglo.
    """

    def __init__(self, elementos=None):
        if elementos is None:
            self._datos = []
        elif isinstance(elementos, Arreglo):
            self._datos = list(elementos._datos)
        elif isinstance(elementos, (list, tuple)):
            self._datos = list(elementos)
        else:
            self._datos = [elementos]

    def __len__(self):
        return len(self._datos)

    def __getitem__(self, indice):
        if isinstance(indice, slice):
            return Arreglo(self._datos[indice])
        return self._datos[indice]

    def __iter__(self):
        return iter(self._datos)

    def __repr__(self):
        return f"Arreglo({self._datos})"

    def a_lista(self):
        """Devuelve los datos como lista nativa de Python."""
        return list(self._datos)

    def mapear(self, funcion):
        """
        Aplica una función a cada elemento y devuelve un nuevo Arreglo (map).
        """
        return Arreglo([funcion(x) for x in self._datos])

    def filtrar(self, predicado):
        """
        Conserva solo los elementos que cumplen con el predicado booleano (filter).
        """
        return Arreglo([x for x in self._datos if predicado(x)])

    def reducir(self, funcion, inicial=None):
        """
        Acumula los elementos usando una función binaria (reduce / fold).
        """
        if not self._datos and inicial is None:
            raise ValueError("No se puede reducir un Arreglo vacío sin valor inicial")

        it = iter(self._datos)
        acumulador = inicial if inicial is not None else next(it)
        for elemento in it:
            acumulador = funcion(acumulador, elemento)
        return acumulador

    def sumar(self):
        """Suma todos los elementos numéricos del arreglo."""
        return sum(x for x in self._datos if isinstance(x, (int, float)))

    def promedio(self):
        """Calcula el promedio aritmético de los elementos."""
        numeros = [x for x in self._datos if isinstance(x, (int, float))]
        return (sum(numeros) / len(numeros)) if numeros else 0.0

    def minimo(self):
        """Obtiene el valor mínimo."""
        numeros = [x for x in self._datos if isinstance(x, (int, float))]
        return min(numeros) if numeros else None

    def maximo(self):
        """Obtiene el valor máximo."""
        numeros = [x for x in self._datos if isinstance(x, (int, float))]
        return max(numeros) if numeros else None
