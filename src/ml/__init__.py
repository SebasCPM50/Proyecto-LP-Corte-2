"""
Paquete de Machine Learning Artesanal para Arcanum.
Contiene:
- RegresionLineal: Predicción supervisada continua (Mínimos Cuadrados).
- KNNClasificador: Clasificación supervisada discreta (K-Vecinos más cercanos).
- KMediasClustering: Agrupamiento no supervisado (K-Means).
"""

from ml.regresion import RegresionLineal
from ml.clasificacion import KNNClasificador
from ml.clustering import KMediasClustering

__all__ = ["RegresionLineal", "KNNClasificador", "KMediasClustering"]
