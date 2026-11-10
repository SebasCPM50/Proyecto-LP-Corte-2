"""
Módulo de Clasificación KNN (K-Nearest Neighbors para Arcanum)
Algoritmo de clasificación supervisada 100% artesanal sin scikit-learn.
Clasifica nuevos registros calculando la distancia euclidiana a las muestras conocidas
y asignando la clase por votación mayoritaria entre los K vecinos más cercanos.
"""

import math
from collections import Counter


class KNNClasificador:
    """
    Clasificador K-Vecinos más Cercanos.
    """

    def __init__(self, k=3):
        self.k = int(k)
        self.datos_x = []
        self.etiquetas_y = []
        self.esta_entrenado = False

    def entrenar(self, datos_x, etiquetas_y):
        """
        Guarda los puntos de entrenamiento y sus etiquetas de clase correspondientes.
        """
        if len(datos_x) != len(etiquetas_y):
            raise ValueError("La cantidad de registros de entrada no coincide con las etiquetas")
        if len(datos_x) < self.k:
            raise ValueError(f"Se necesitan al menos {self.k} muestras para K={self.k}")

        self.datos_x = [
            [float(v) for v in fila] if hasattr(fila, "__iter__") and not isinstance(fila, (str, bytes))
            else [float(fila)]
            for fila in datos_x
        ]
        self.etiquetas_y = [str(e) for e in etiquetas_y]
        self.esta_entrenado = True
        return self

    @staticmethod
    def _distancia_euclidiana(punto_a, punto_b):
        """Calcula la distancia geométrica euclidiana entre dos puntos: sqrt(sum((a_i - b_i)^2))."""
        suma = sum((float(a) - float(b)) ** 2 for a, b in zip(punto_a, punto_b))
        return math.sqrt(suma)

    def predecir(self, nuevo_punto):
        """
        Clasifica un nuevo punto encontrando sus K vecinos más cercanos
        y devolviendo la etiqueta ganadora por votación de mayoría.
        """
        if not self.esta_entrenado:
            raise RuntimeError("El clasificador KNN no ha sido entrenado")

        vector_p = (
            [float(v) for v in nuevo_punto]
            if hasattr(nuevo_punto, "__iter__") and not isinstance(nuevo_punto, (str, bytes))
            else [float(nuevo_punto)]
        )

        # Calculamos distancia a todos los puntos de entrenamiento
        distancias = []
        for idx, muestra in enumerate(self.datos_x):
            d = self._distancia_euclidiana(vector_p, muestra)
            distancias.append((d, self.etiquetas_y[idx]))

        # Ordenamos de menor a mayor distancia
        distancias.sort(key=lambda item: item[0])

        # Tomamos los K vecinos más cercanos
        vecinos_k = [etiqueta for _, etiqueta in distancias[:self.k]]

        # Votación por mayoría (moda)
        conteo = Counter(vecinos_k)
        etiqueta_ganadora, _ = conteo.most_common(1)[0]
        return etiqueta_ganadora

    def predecir_lote(self, lista_puntos):
        """Clasifica un lote de nuevos registros."""
        return [self.predecir(p) for p in lista_puntos]

    def __repr__(self):
        estado = f"K={self.k}, {len(self.datos_x)} muestras" if self.esta_entrenado else "no entrenado"
        return f"<KNNClasificador: {estado}>"
