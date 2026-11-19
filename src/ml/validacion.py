"""Validaciones compartidas para evitar resultados silenciosamente incorrectos."""
import math


def positivo_entero(valor, nombre):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValueError(f"{nombre} debe ser un entero positivo")
    return valor


def vector(datos):
    if isinstance(datos, (str, bytes)):
        raise ValueError("Se esperan números, no texto")
    valores = list(datos) if hasattr(datos, "__iter__") else [datos]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in valores):
        raise ValueError("Los datos deben ser numéricos y no tener nulos")
    valores = [float(v) for v in valores]
    if not valores or any(not math.isfinite(v) for v in valores):
        raise ValueError("Los datos deben contener números finitos y no estar vacíos")
    return valores


def matriz(datos):
    puntos = [vector(fila) for fila in datos]
    if not puntos or any(len(f) != len(puntos[0]) for f in puntos):
        raise ValueError("Los datos deben ser no vacíos y todas las filas deben tener igual dimensión")
    return puntos
