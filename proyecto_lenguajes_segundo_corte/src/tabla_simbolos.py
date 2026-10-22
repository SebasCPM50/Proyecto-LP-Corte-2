"""
Módulo de la Tabla de Símbolos para Arcanum
Es como la memoria del programa donde guardamos los nombres de las variables,
qué tipo de dato tienen y el valor que llevan guardado
Todo hecho con diccionarios de Python sin usar librerías raras
"""

from errores import ErrorSemantico
from pocion import Pocion


class Simbolo:
    """
    Representa una sola variable guardada en memoria
    Guarda su nombre, su tipo, el valor real y en qué línea del archivo se creó
    """
    def __init__(self, nombre, tipo, valor, linea=None, columna=None):
        # Acá guardamos el nombre de la variable como 'ventas' o 'x'
        self.nombre = nombre
        # Acá guardamos si es 'POCION', 'NUMERO', 'CADENA' o 'BOOLEANO'
        self.tipo = tipo
        # Acá guardamos el dato real, por ejemplo el objeto Pocion o el número
        self.valor = valor
        # Guardamos la línea y columna para saber de dónde salió
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        # Texto bonito para cuando queramos ver qué tiene la variable
        if self.tipo == "POCION":
            filas = len(self.valor)
            cols = self.valor.columnas
            return f"<Simbolo {self.nombre} ({self.tipo}): {filas} filas, ingredientes={cols}>"
        return f"<Simbolo {self.nombre} ({self.tipo}): {self.valor}>"


class TablaSimbolos:
    """
    Acá manejamos el diccionario con todas las variables del programa
    Nos sirve para revisar que nadie use variables inventadas o tipos incompatibles
    """
    def __init__(self):
        # Este diccionario guarda: clave = nombre de la variable, valor = objeto Simbolo
        self._simbolos = {}

    def definir(self, nombre, valor, tipo_sugerido=None, linea=None, columna=None):
        # Si no nos dijeron el tipo, lo descubrimos nosotros mismos mirando el valor
        if tipo_sugerido is None:
            tipo_sugerido = self.determinar_tipo(valor)

        # Creamos el símbolo y lo metemos en el diccionario para no perderlo
        simbolo = Simbolo(nombre, tipo_sugerido, valor, linea, columna)
        self._simbolos[nombre] = simbolo
        return simbolo

    def determinar_tipo(self, valor):
        # Mira qué cosa es en Python y le asigna el nombre alquímico correspondiente
        if isinstance(valor, Pocion):
            return "POCION"
        elif isinstance(valor, bool):
            return "BOOLEANO"
        elif isinstance(valor, (int, float)):
            return "NUMERO"
        elif isinstance(valor, str):
            return "CADENA"
        return "DESCONOCIDO"

    def existe(self, nombre):
        # Nos dice True si la variable ya fue creada antes en la memoria
        return nombre in self._simbolos

    def obtener(self, nombre, linea=None, columna=None):
        # Busca la variable en el diccionario, y si no está tira un error semántico claro
        if nombre not in self._simbolos:
            raise ErrorSemantico(
                f"La variable o poción '{nombre}' no ha sido declarada o invocada previamente",
                linea, columna
            )
        return self._simbolos[nombre]

    def obtener_valor(self, nombre, linea=None, columna=None):
        # Saca directo el valor que tiene adentro la variable
        return self.obtener(nombre, linea, columna).valor

    def obtener_pocion(self, nombre, linea=None, columna=None):
        # Busca la variable pero además revisa que sí sea una Poción (tabla de datos)
        # Si alguien intenta hacer operaciones de tabla sobre un número, acá lo frena
        simbolo = self.obtener(nombre, linea, columna)
        if simbolo.tipo != "POCION" or not isinstance(simbolo.valor, Pocion):
            raise ErrorSemantico(
                f"La variable '{nombre}' es de tipo {simbolo.tipo}, no es una POCIÓN (tabla de datos)",
                linea, columna
            )
        return simbolo.valor

    def verificar_columna(self, nombre_pocion, nombre_columna, linea=None, columna=None):
        # Revisa que la columna que piden sí exista dentro de la tabla
        # Si no existe, le avisa al usuario cuáles sí están disponibles
        pocion = self.obtener_pocion(nombre_pocion, linea, columna)
        if nombre_columna not in pocion.columnas:
            columnas_disponibles = list(pocion.columnas)
            raise ErrorSemantico(
                f"La poción '{nombre_pocion}' no contiene el ingrediente (columna) '{nombre_columna}' (Disponibles: {columnas_disponibles})",
                linea, columna
            )
        return True

    def verificar_columnas(self, nombre_pocion, lista_columnas, linea=None, columna=None):
        # Hace la misma revisión pero para una lista completa de columnas
        for col in lista_columnas:
            self.verificar_columna(nombre_pocion, col, linea, columna)

    def limpiar(self):
        # Borra todo lo que tengamos en memoria
        self._simbolos.clear()

    def listar_simbolos(self):
        # Devuelve la lista con todos los símbolos que existen
        return list(self._simbolos.values())

    def imprimir(self):
        # Muestra en la terminal qué variables quedaron guardadas al final de la corrida
        print()
        print("[ESTADO DE LA TABLA DE SÍMBOLOS]")
        if not self._simbolos:
            print("  (Tabla vacía)")
            return
        for nombre, simb in self._simbolos.items():
            if simb.tipo == "POCION":
                pocion = simb.valor
                print(f"  * {nombre} -> POCION [{len(pocion)} filas x {len(pocion.columnas)} columnas]: {pocion.columnas}")
            else:
                print(f"  * {nombre} -> {simb.tipo} = {simb.valor}")
        print()
