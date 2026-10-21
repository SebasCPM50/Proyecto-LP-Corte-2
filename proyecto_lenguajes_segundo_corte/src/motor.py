"""
Módulo del Motor de Procesamiento Alquímico — Arcanum
=====================================================
Fachada que gestiona las transformaciones sobre datos sin ninguna librería externa.
Se apoya en la clase Pocion implementada desde cero con listas y diccionarios nativos.
"""

from pocion import Pocion


class MotorDatos:
    """
    Fachada que conecta las operaciones del Visitor con la estructura artesanal Pocion.
    """

    @staticmethod
    def cargar_csv(ruta, linea=None, columna=None):
        return Pocion.desde_csv(ruta, linea, columna)

    @staticmethod
    def guardar_csv(pocion, ruta, linea=None, columna=None):
        return pocion.a_csv(ruta, linea, columna)

    @staticmethod
    def recolectar(pocion, columnas):
        return pocion.recolectar(columnas)

    @staticmethod
    def purificar(pocion, evaluador_condicion):
        return pocion.purificar(evaluador_condicion)

    @staticmethod
    def ordenar(pocion, columna, ascendente=True):
        return pocion.ordenar(columna, ascendente)

    @staticmethod
    def transmutar(pocion, nombre_columna, evaluador_expresion):
        return pocion.transmutar(nombre_columna, evaluador_expresion)

    @staticmethod
    def sanar_descartar_nulos(pocion):
        return pocion.sanar_descartar_nulos()

    @staticmethod
    def sanar_llenar_nulos(pocion, columna, valor):
        return pocion.sanar_llenar_nulos(columna, valor)

    @staticmethod
    def destilar(pocion, columnas_grupo, lista_agregaciones):
        return pocion.destilar(columnas_grupo, lista_agregaciones)

    @staticmethod
    def describir(pocion):
        return pocion.describir()
