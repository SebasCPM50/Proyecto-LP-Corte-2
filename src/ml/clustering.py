"""
Módulo de K-Means Clustering (Algoritmo de Agrupamiento no supervisado para Arcanum)
Implementación 100% matemática y artesanal sin scikit-learn.
Agrupa datos multidimensionales en K grupos calculando centroides de forma iterativa.
"""

import math


class KMediasClustering:
    """
    Algoritmo de aprendizaje no supervisado K-Means.
    Descubre agrupaciones naturales (clusters) sin requerir etiquetas previas.
    """

    def __init__(self, k=2, max_iter=30):
        self.k = int(k)
        self.max_iter = int(max_iter)
        self.centroides = []
        self.asignaciones = []
        self.esta_entrenado = False

    @staticmethod
    def _distancia_euclidiana(punto_a, punto_b):
        return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(punto_a, punto_b)))

    def agrupar(self, datos):
        """
        Ejecuta el algoritmo de agrupamiento K-Means sobre una lista de vectores numéricos.
        Retorna la lista de asignaciones de cluster para cada punto.
        """
        matriz_puntos = [
            [float(v) for v in fila]
            if hasattr(fila, "__iter__") and not isinstance(fila, (str, bytes))
            else [float(fila)]
            for fila in datos
        ]
        n = len(matriz_puntos)
        if n < self.k:
            raise ValueError(f"No hay suficientes datos ({n}) para formar K={self.k} grupos")

        dimension = len(matriz_puntos[0])

        # 1. Inicialización determinista y bien distribuida de centroides
        paso = max(1, n // self.k)
        self.centroides = [list(matriz_puntos[min(i * paso, n - 1)]) for i in range(self.k)]

        # 2. Bucle iterativo de convergencia
        self.asignaciones = [0] * n
        for _ in range(self.max_iter):
            hubo_cambios = False

            # Paso A: Asignar cada punto al centroide más cercano
            for idx, punto in enumerate(matriz_puntos):
                distancias = [self._distancia_euclidiana(punto, c) for c in self.centroides]
                cluster_cercano = distancias.index(min(distancias))
                if self.asignaciones[idx] != cluster_cercano:
                    self.asignaciones[idx] = cluster_cercano
                    hubo_cambios = True

            # Si ningún punto cambió de grupo, hemos convergido
            if not hubo_cambios:
                break

            # Paso B: Recalcular la posición de cada centroide como el promedio del cluster
            nuevos_centroides = []
            for c_idx in range(self.k):
                puntos_cluster = [matriz_puntos[i] for i in range(n) if self.asignaciones[i] == c_idx]
                if puntos_cluster:
                    centroide_prom = [
                        sum(p[d] for p in puntos_cluster) / len(puntos_cluster)
                        for d in range(dimension)
                    ]
                    nuevos_centroides.append(centroide_prom)
                else:
                    nuevos_centroides.append(self.centroides[c_idx])

            self.centroides = nuevos_centroides

        self.esta_entrenado = True
        return self.asignaciones

    def asignar_a_pocion(self, pocion, columnas, nombre_columna="cluster"):
        """
        Aplica K-Means sobre las columnas numéricas de una Poción
        y devuelve una nueva Poción con la columna de cluster añadida.
        """
        from pocion import Pocion
        puntos = []
        for fila in pocion.filas:
            puntos.append([fila.get(c, 0.0) for c in columnas])

        etiquetas_cluster = self.agrupar(puntos)

        nuevas_filas = []
        for fila, c_id in zip(pocion.filas, etiquetas_cluster):
            copia = fila.copy()
            copia[nombre_columna] = f"Cluster_{c_id + 1}"
            nuevas_filas.append(copia)

        nuevas_cols = list(pocion.columnas)
        if nombre_columna not in nuevas_cols:
            nuevas_cols.append(nombre_columna)

        return Pocion(nuevas_cols, nuevas_filas)

    def __repr__(self):
        estado = f"K={self.k}, centroides={len(self.centroides)}" if self.esta_entrenado else "no entrenado"
        return f"<KMediasClustering: {estado}>"
