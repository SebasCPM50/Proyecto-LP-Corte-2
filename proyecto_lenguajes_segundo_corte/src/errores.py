"""
Manejador de errores para Arcanum
Acá atrapamos las cosas que salgan mal para explicárselas al usuario de forma clara
sin que la terminal tire un error feo de Python
"""

from antlr4.error.ErrorListener import ErrorListener


class ErrorSemantico(Exception):
    """
    Esta excepción la usamos cuando hay un error de lógica en el código de Arcanum
    Por ejemplo si alguien usa una variable que no existe o quiere sumar texto con números
    """
    def __init__(self, mensaje, linea=None, columna=None):
        super().__init__(mensaje)
        # Guardamos el mensaje y la posición exacta en el archivo para avisarle al usuario
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def __str__(self):
        # Armamos el texto del error mostrando en qué línea y columna ocurrió
        if self.linea is not None and self.columna is not None:
            return f"[Error Semántico] Línea {self.linea}, Columna {self.columna}: {self.mensaje}"
        elif self.linea is not None:
            return f"[Error Semántico] Línea {self.linea}: {self.mensaje}"
        return f"[Error Semántico] {self.mensaje}"


class ManejadorErrores(ErrorListener):
    """
    Acá escuchamos los errores que detecta ANTLR (si escriben mal una palabra o falta un punto y coma)
    y los pasamos a mensajes en español entendibles
    """
    def __init__(self):
        super().__init__()
        # Lista donde vamos guardando los errores que vayan saliendo
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Acá traducimos los mensajes raros de ANTLR en inglés a algo normal en español
        mensaje_limpio = msg
        if "mismatched input" in msg:
            mensaje_limpio = f"Token inesperado cerca de {offendingSymbol.text if offendingSymbol else ''}"
        elif "no viable alternative" in msg:
            mensaje_limpio = f"Instrucción incompleta o no reconocida cerca de {offendingSymbol.text if offendingSymbol else ''}"
        elif "extraneous input" in msg:
            mensaje_limpio = f"Elemento sobrante: {offendingSymbol.text if offendingSymbol else ''}"

        # Guardamos el detalle con la línea y columna para que se sepa dónde corregir
        texto = f"Línea {line}, Columna {column}: {mensaje_limpio} (Detalle: {msg})"
        self.errores.append(texto)

    def hay_errores(self):
        # Nos dice True si hubo al menos un fallo de escritura o sintaxis
        return len(self.errores) > 0

    def imprimir(self):
        # Imprime la lista de errores en pantalla
        for err in self.errores:
            print(f"  * {err}")
