"""
Módulo de Matriz (Álgebra Lineal Artesanal para Arcanum)
Nuestra propia versión de NumPy implementada 100% en Python puro,
sin usar la librería numpy ni scipy.
"""


class Matriz:
    """
    Representa una matriz bidimensional de números.
    Soporta operaciones de álgebra lineal: suma, resta, transpuesta,
    multiplicación matricial y estimación por mínimos cuadrados.
    """

    def __init__(self, datos):
        if isinstance(datos, Matriz):
            self.filas_datos = [list(f) for f in datos.filas_datos]
        elif hasattr(datos, "__iter__"):
            filas_convertidas = []
            for fila in datos:
                if hasattr(fila, "__iter__") and not isinstance(fila, (str, bytes)):
                    filas_convertidas.append([float(val) if val is not None else 0.0 for val in fila])
                else:
                    filas_convertidas.append([float(fila) if fila is not None else 0.0])
            self.filas_datos = filas_convertidas
        else:
            raise TypeError("Los datos de la matriz deben ser una colección bidimensional o lista de filas")

        self.filas = len(self.filas_datos)
        self.columnas = len(self.filas_datos[0]) if self.filas > 0 else 0

    @property
    def dimensiones(self):
        """Retorna una tupla con (filas, columnas)."""
        return (self.filas, self.columnas)

    def __getitem__(self, indice):
        return self.filas_datos[indice]

    def __len__(self):
        return self.filas

    def __repr__(self):
        lineas = []
        for fila in self.filas_datos:
            vals = "  ".join(f"{v:8.2f}" for v in fila)
            lineas.append(f"  [ {vals} ]")
        return f"<Matriz {self.filas}x{self.columnas}>\n" + "\n".join(lineas)

    def obtener_fila(self, i):
        """Retorna una fila como lista simple."""
        return list(self.filas_datos[i])

    def obtener_columna(self, j):
        """Retorna una columna como lista simple."""
        return [self.filas_datos[i][j] for i in range(self.filas)]

    def transpuesta(self):
        """Calcula y retorna la matriz transpuesta (A^T)."""
        nuevas = []
        for j in range(self.columnas):
            nuevas.append(self.obtener_columna(j))
        return Matriz(nuevas)

    def sumar(self, otra):
        """Suma elemento por elemento dos matrices de dimensiones idénticas."""
        otra_matriz = otra if isinstance(otra, Matriz) else Matriz(otra)
        if self.dimensiones != otra_matriz.dimensiones:
            raise ValueError(f"Dimensiones incompatibles para suma: {self.dimensiones} vs {otra_matriz.dimensiones}")

        res = []
        for i in range(self.filas):
            fila_res = [self.filas_datos[i][j] + otra_matriz.filas_datos[i][j] for j in range(self.columnas)]
            res.append(fila_res)
        return Matriz(res)

    def restar(self, otra):
        """Resta elemento por elemento dos matrices."""
        otra_matriz = otra if isinstance(otra, Matriz) else Matriz(otra)
        if self.dimensiones != otra_matriz.dimensiones:
            raise ValueError(f"Dimensiones incompatibles para resta: {self.dimensiones} vs {otra_matriz.dimensiones}")

        res = []
        for i in range(self.filas):
            fila_res = [self.filas_datos[i][j] - otra_matriz.filas_datos[i][j] for j in range(self.columnas)]
            res.append(fila_res)
        return Matriz(res)

    def multiplicar_escalar(self, k):
        """Multiplica todos los elementos por un número escalar k."""
        k_num = float(k)
        res = [[val * k_num for val in fila] for fila in self.filas_datos]
        return Matriz(res)

    def multiplicar(self, otra):
        """
        Multiplicación matricial estándar (producto punto) O(N*M*P).
        Requiere que las columnas de self sean iguales a las filas de otra.
        """
        otra_matriz = otra if isinstance(otra, Matriz) else Matriz(otra)
        if self.columnas != otra_matriz.filas:
            raise ValueError(
                f"No se pueden multiplicar matrices: columnas de A ({self.columnas}) "
                f"!= filas de B ({otra_matriz.filas})"
            )

        filas_a, cols_a = self.filas, self.columnas
        cols_b = otra_matriz.columnas
        res = [[0.0 for _ in range(cols_b)] for _ in range(filas_a)]

        for i in range(filas_a):
            for j in range(cols_b):
                suma = 0.0
                for k in range(cols_a):
                    suma += self.filas_datos[i][k] * otra_matriz.filas_datos[k][j]
                res[i][j] = round(suma, 4)
        return Matriz(res)

    @staticmethod
    def desde_pocion(pocion, columnas):
        """
        Extrae las columnas numéricas solicitadas de una Poción y construye una Matriz.
        """
        filas_matriz = []
        for fila in pocion.filas:
            fila_num = []
            for col in columnas:
                val = fila.get(col)
                if val is None or not isinstance(val, (int, float)):
                    fila_num.append(0.0)
                else:
                    fila_num.append(float(val))
            filas_matriz.append(fila_num)
        return Matriz(filas_matriz)
