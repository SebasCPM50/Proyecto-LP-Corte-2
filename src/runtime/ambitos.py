"""Resolución uniforme de variables locales, columnas y símbolos globales."""
from errores import ErrorSemantico
from pocion import Pocion

class Ambitos:
    def obtener_valor(self, nombre, linea=None, columna=None):
        if self._marcos_locales and nombre in self._marcos_locales[-1]:
            return self._marcos_locales[-1][nombre]
        if self._fila_activa is not None and nombre in self._fila_activa:
            return self._fila_activa[nombre]
        if self.tabla.existe(nombre):
            return self.tabla.obtener_valor(nombre, linea, columna)
        if self._fila_activa is not None:
            raise ErrorSemantico(f"El ingrediente '{nombre}' no existe en la poción activa ni como variable declarada (Disponibles: {list(self._fila_activa)})", linea, columna)
        return self.tabla.obtener_valor(nombre, linea, columna)

    def obtener_pocion(self, nombre, linea=None, columna=None):
        valor = self.obtener_valor(nombre, linea, columna)
        if not isinstance(valor, Pocion):
            raise ErrorSemantico(f"La variable '{nombre}' no es una POCIÓN (tabla de datos)", linea, columna)
        return valor

    def verificar_columna(self, nombre, campo, linea=None, columna=None):
        tabla = self.obtener_pocion(nombre, linea, columna)
        if campo not in tabla.columnas:
            raise ErrorSemantico(f"La poción '{nombre}' no contiene el ingrediente (columna) '{campo}' (Disponibles: {tabla.columnas})", linea, columna)

    def verificar_columnas(self, nombre, campos, linea=None, columna=None):
        for campo in campos:
            self.verificar_columna(nombre, campo, linea, columna)
