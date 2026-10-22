"""
Motor de datos para Arcanum
Es como un puente para conectar lo que viene del árbol de ANTLR (Visitor)
con nuestra clase Pocion hecha desde cero sin usar Pandas ni NumPy
"""

from pocion import Pocion


class MotorDatos:
    """
    Acá agrupamos los métodos principales para manipular tablas de datos
    Simplemente llama al método correspondiente dentro de Pocion
    """

    @staticmethod
    def cargar_csv(ruta, linea=None, columna=None):
        # Abre y carga los datos de un archivo CSV en disco
        return Pocion.desde_csv(ruta, linea, columna)

    @staticmethod
    def guardar_csv(pocion, ruta, linea=None, columna=None):
        # Guarda la tabla actual en un archivo CSV nuevo
        return pocion.a_csv(ruta, linea, columna)

    @staticmethod
    def recolectar(pocion, columnas):
        # Elige solo las columnas que el usuario pidió
        return pocion.recolectar(columnas)

    @staticmethod
    def purificar(pocion, evaluador_condicion):
        # Filtra las filas que cumplan la condición que pasamos
        return pocion.purificar(evaluador_condicion)

    @staticmethod
    def ordenar(pocion, columna, ascendente=True):
        # Ordena las filas según el valor de una columna
        return pocion.ordenar(columna, ascendente)

    @staticmethod
    def transmutar(pocion, nombre_columna, evaluador_expresion):
        # Agrega una columna nueva calculando su valor fila por fila
        return pocion.transmutar(nombre_columna, evaluador_expresion)

    @staticmethod
    def sanar_descartar_nulos(pocion):
        # Quita todas las filas que tengan casillas vacías o nulas
        return pocion.sanar_descartar_nulos()

    @staticmethod
    def sanar_llenar_nulos(pocion, columna, valor):
        # Si hay celdas vacías en una columna, les pone un valor por defecto
        return pocion.sanar_llenar_nulos(columna, valor)

    @staticmethod
    def destilar(pocion, columnas_grupo, lista_agregaciones):
        # Agrupa filas por categorías y calcula sumas, promedios, etc
        return pocion.destilar(columnas_grupo, lista_agregaciones)

    @staticmethod
    def describir(pocion):
        # Saca un resumen con promedio, mínimo, máximo y desviación
        return pocion.describir()

    @staticmethod
    def muestra_aleatoria(pocion, cantidad):
        # Saca varias filas al azar de la tabla
        return pocion.muestra_aleatoria(cantidad)

    @staticmethod
    def azar(minimo=0, maximo=1):
        # Saca un número aleatorio entre mínimo y máximo
        from pocion import numero_aleatorio
        return numero_aleatorio(minimo, maximo)

