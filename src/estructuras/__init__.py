"""
Paquete de Estructuras de Datos Artesanales para Arcanum.
Contiene:
- Arreglo: Vector funcional (map, filter, reduce).
- Matriz: Álgebra lineal bidimensional (versión propia de NumPy).
- Pocion: DataFrame relacional e inmutable (versión propia de Pandas).
"""

from estructuras.arreglo import Arreglo
from estructuras.matriz import Matriz
from pocion import Pocion

__all__ = ["Arreglo", "Matriz", "Pocion"]
