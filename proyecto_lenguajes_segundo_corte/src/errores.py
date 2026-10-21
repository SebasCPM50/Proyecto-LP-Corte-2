"""
Módulo de Manejo de Errores — Arcanum
=====================================
Este módulo se encarga de capturar y presentar de forma amigable los errores
que puedan ocurrir al procesar un programa escrito en Arcanum:
1. Errores léxicos y sintácticos (detectados por ANTLR).
2. Errores semánticos (detectados durante la ejecución con la Tabla de Símbolos y el Visitor).
"""

from antlr4.error.ErrorListener import ErrorListener


class ErrorSemantico(Exception):
    """
    Excepción lanzada cuando ocurre un error de significado o lógica en Arcanum.
    Ejemplos:
    - Usar una variable que no ha sido definida.
    - Intentar seleccionar una columna que no existe en la poción.
    - Operar tipos incompatibles (sumar texto con número).
    - Cargar un archivo CSV inexistente.
    """
    def __init__(self, mensaje, linea=None, columna=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def __str__(self):
        if self.linea is not None and self.columna is not None:
            return f"[Error Semántico] Línea {self.linea}, Columna {self.columna}: {self.mensaje}"
        elif self.linea is not None:
            return f"[Error Semántico] Línea {self.linea}: {self.mensaje}"
        return f"[Error Semántico] {self.mensaje}"


class ManejadorErrores(ErrorListener):
    """
    Captura los errores léxicos y sintácticos directamente desde ANTLR
    para presentarlos con mensajes comprensibles en español.
    """
    def __init__(self):
        super().__init__()
        self.errores = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Traducimos o simplificamos algunos mensajes técnicos comunes de ANTLR
        mensaje_limpio = msg
        if "mismatched input" in msg:
            mensaje_limpio = f"Token inesperado cerca de {offendingSymbol.text if offendingSymbol else ''}"
        elif "no viable alternative" in msg:
            mensaje_limpio = f"Instrucción incompleta o no reconocida cerca de {offendingSymbol.text if offendingSymbol else ''}"
        elif "extraneous input" in msg:
            mensaje_limpio = f"Elemento sobrante: {offendingSymbol.text if offendingSymbol else ''}"

        texto = f"Línea {line}, Columna {column}: {mensaje_limpio} (Detalle: {msg})"
        self.errores.append(texto)

    def hay_errores(self):
        """Retorna True si hubo al menos un error detectado."""
        return len(self.errores) > 0

    def imprimir(self):
        """Imprime todos los errores recolectados."""
        for err in self.errores:
            print(f"  - {err}")
