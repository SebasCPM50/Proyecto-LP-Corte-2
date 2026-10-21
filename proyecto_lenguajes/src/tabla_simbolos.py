"""
Módulo de Tabla de Símbolos — Arcanum
=====================================
La Tabla de Símbolos es la libreta de memoria del intérprete.
Guarda los nombres de todas las variables (pociones, números, textos, booleanos),
sus tipos y sus valores actuales.

100% LIBRE DE LIBRERÍAS EXTERNAS:
Utiliza nuestra propia clase Pocion para las estructuras tabulares.
"""

from errores import ErrorSemantico
from pocion import Pocion


class Simbolo:
    """
    Representa una variable individual en la memoria de Arcanum.
    """
    def __init__(self, nombre, tipo, valor, linea=None, columna=None):
        self.nombre = nombre       # Nombre de la variable (ej. 'ventas')
        self.tipo = tipo           # 'POCION', 'NUMERO', 'CADENA', 'BOOLEANO'
        self.valor = valor         # El valor real (Pocion, float, int, str, bool)
        self.linea = linea         # Línea donde se definió
        self.columna = columna     # Columna donde se definió

    def __repr__(self):
        if self.tipo == "POCION":
            filas = len(self.valor)
            cols = self.valor.columnas
            return f"<Simbolo {self.nombre} ({self.tipo}): {filas} filas, ingredientes={cols}>"
        return f"<Simbolo {self.nombre} ({self.tipo}): {self.valor}>"


class TablaSimbolos:
    """
    Gestiona el almacenamiento y validación semántica de todas las variables.
    """
    def __init__(self):
        # Diccionario principal: clave = nombre_variable, valor = objeto Simbolo
        self._simbolos = {}

    def definir(self, nombre, valor, tipo_sugerido=None, linea=None, columna=None):
        """
        Registra o actualiza una variable en la tabla de símbolos.
        Deduce el tipo automáticamente si no se especifica.
        """
        if tipo_sugerido is None:
            tipo_sugerido = self.determinar_tipo(valor)

        simbolo = Simbolo(nombre, tipo_sugerido, valor, linea, columna)
        self._simbolos[nombre] = simbolo
        return simbolo

    def determinar_tipo(self, valor):
        """
        Identifica el tipo semántico de Arcanum según el valor de Python.
        """
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
        """Verifica si una variable existe en la tabla."""
        return nombre in self._simbolos

    def obtener(self, nombre, linea=None, columna=None):
        """
        Recupera el símbolo de la tabla.
        Si no existe, lanza un ErrorSemantico claro.
        """
        if nombre not in self._simbolos:
            raise ErrorSemantico(
                f"La variable o poción '{nombre}' no ha sido declarada o invocada previamente.",
                linea, columna
            )
        return self._simbolos[nombre]

    def obtener_valor(self, nombre, linea=None, columna=None):
        """Recupera el valor directo de una variable."""
        return self.obtener(nombre, linea, columna).valor

    def obtener_pocion(self, nombre, linea=None, columna=None):
        """
        Recupera una variable verificando que sea de tipo POCION.
        Si es de otro tipo, lanza un error semántico explicativo.
        """
        simbolo = self.obtener(nombre, linea, columna)
        if simbolo.tipo != "POCION" or not isinstance(simbolo.valor, Pocion):
            raise ErrorSemantico(
                f"La variable '{nombre}' es de tipo {simbolo.tipo}, no es una POCIÓN (tabla de datos). "
                f"Esta operación requiere una poción de datos.",
                linea, columna
            )
        return simbolo.valor

    def verificar_columna(self, nombre_pocion, nombre_columna, linea=None, columna=None):
        """
        Verifica que una columna (ingrediente) exista dentro de una poción.
        Si no existe, informa el error y lista las columnas disponibles.
        """
        pocion = self.obtener_pocion(nombre_pocion, linea, columna)
        if nombre_columna not in pocion.columnas:
            columnas_disponibles = list(pocion.columnas)
            raise ErrorSemantico(
                f"La poción '{nombre_pocion}' no contiene el ingrediente (columna) '{nombre_columna}'. "
                f"Columnas disponibles en la poción: {columnas_disponibles}",
                linea, columna
            )
        return True

    def verificar_columnas(self, nombre_pocion, lista_columnas, linea=None, columna=None):
        """Verifica una lista de columnas en una poción."""
        for col in lista_columnas:
            self.verificar_columna(nombre_pocion, col, linea, columna)

    def limpiar(self):
        """Limpia todos los símbolos guardados en memoria."""
        self._simbolos.clear()

    def listar_simbolos(self):
        """Retorna una lista legible de todos los símbolos actuales."""
        return list(self._simbolos.values())

    def imprimir(self):
        """Imprime la tabla de símbolos en consola con formato prolijo."""
        print("\n--- [ESTADO DE LA TABLA DE SÍMBOLOS] ---")
        if not self._simbolos:
            print("  (Tabla vacía)")
            return
        for nombre, simb in self._simbolos.items():
            if simb.tipo == "POCION":
                pocion = simb.valor
                print(f"  * {nombre} -> POCION [{len(pocion)} filas x {len(pocion.columnas)} columnas]: {pocion.columnas}")
            else:
                print(f"  * {nombre} -> {simb.tipo} = {simb.valor}")
        print("-----------------------------------------\n")
