"""Generador congruencial usado por las funciones de azar."""
import os

# Semilla inicial para generar números aleatorios sin importar ninguna librería externa
_semilla_azar = (id(object()) * 31 + os.getpid()) & 0x7fffffff


def _generar_siguiente_azar():
    # Algoritmo matemático congruencial para sacar números al azar hecho a mano sin librerías
    global _semilla_azar
    _semilla_azar = (_semilla_azar * 1103515245 + 12345) & 0x7fffffff
    return _semilla_azar


def numero_aleatorio(minimo=0, maximo=1):
    # Genera un número al azar entre un mínimo y un máximo
    # Si no le pasan parámetros devuelve un decimal entre 0 y 1
    if minimo > maximo:
        raise ValueError("El mínimo no puede superar el máximo")
    azar_crudo = _generar_siguiente_azar() / 2147483648.0
    if minimo == 0 and maximo == 1:
        return round(azar_crudo, 4)
    if isinstance(minimo, int) and isinstance(maximo, int):
        rango = (maximo - minimo) + 1
        return minimo + int(azar_crudo * rango)
    return round(minimo + azar_crudo * (maximo - minimo), 4)



