"""Registro extensible de funciones del lenguaje, separado del recorrido ANTLR."""
import math
from errores import ErrorSemantico
from estructuras.arreglo import Arreglo
from estructuras.matriz import Matriz
from pocion import Pocion, numero_aleatorio


class RegistroNativas:
    def __init__(self):
        self.funciones = {}

    def registrar(self, nombres, minimo, maximo, funcion):
        for nombre in nombres.split():
            self.funciones[nombre] = (minimo, maximo, funcion)

    def __contains__(self, nombre):
        return nombre in self.funciones

    def ejecutar(self, nombre, args, interprete, linea=None, columna=None):
        minimo, maximo, funcion = self.funciones[nombre]
        if not minimo <= len(args) <= maximo:
            raise ErrorSemantico(f"{nombre} espera de {minimo} a {maximo} argumentos; recibió {len(args)}", linea, columna)
        try:
            return funcion(interprete, *args)
        except ErrorSemantico:
            raise
        except (ValueError, TypeError, IndexError, KeyError, AttributeError, RuntimeError, OverflowError) as error:
            raise ErrorSemantico(f"{nombre}: {error}", linea, columna) from error


def entero(valor):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError("Se requiere un número entero")
    return valor


def rango(*args):
    return Arreglo(list(range(*(entero(a) for a in args))))


def tabla(columnas, filas):
    cols = list(columnas)
    if not cols or any(not isinstance(c, str) or not c for c in cols) or len(set(cols)) != len(cols):
        raise ValueError("Las columnas deben ser nombres de texto únicos y no vacíos")
    registros = []
    for fila in filas:
        valores = list(fila)
        if len(valores) != len(cols):
            raise ValueError("Cada fila debe tener tantos valores como columnas")
        registros.append(dict(zip(cols, valores)))
    return Pocion(cols, registros)


def columna(pocion, nombre):
    if not isinstance(pocion, Pocion) or nombre not in pocion.columnas:
        raise ValueError(f"La tabla no contiene la columna '{nombre}'")
    return Arreglo([f.get(nombre) for f in pocion.filas])


def funcional(interprete, operacion, valores, receta, inicial=None):
    if not isinstance(receta, str):
        raise ValueError('Indica el nombre de la receta entre comillas, por ejemplo "doble"')
    arreglo = Arreglo(valores)
    funcion = lambda *args: interprete.llamar(receta, list(args))
    if operacion == "mapear":
        return arreglo.mapear(funcion)
    if operacion == "filtrar":
        return arreglo.filtrar(funcion)
    return arreglo.reducir(funcion, inicial)


def crear_registro():
    r = RegistroNativas()
    def simple(nombres, minimo, maximo, fn):
        r.registrar(nombres, minimo, maximo, lambda interprete, *args: fn(*args))
    simple("random aleatorio azar", 0, 2, lambda *a: numero_aleatorio(*(a if len(a) != 1 else (0, a[0]))))
    simple("arreglo", 0, 1, Arreglo)
    simple("matriz", 1, 1, Matriz)
    simple("transpuesta transponer", 1, 1, lambda m: m.transpuesta())
    simple("sumar_matrices", 2, 2, lambda a, b: a.sumar(b))
    simple("restar_matrices", 2, 2, lambda a, b: a.restar(b))
    simple("multiplicar_matrices", 2, 2, lambda a, b: a.multiplicar(b))
    simple("escalar_matriz", 2, 2, lambda a, k: a.multiplicar_escalar(k))
    simple("longitud len", 1, 1, len)
    simple("rango range", 1, 3, rango)
    simple("anexar", 2, 2, lambda a, x: Arreglo(list(a) + [x]))
    simple("tabla", 2, 2, tabla)
    simple("columna", 2, 2, columna)
    simple("a_matriz", 2, 2, Matriz.desde_pocion)
    simple("exp", 1, 1, lambda x: math.exp(float(x)))
    simple("tanh tan_hiperbolico", 1, 1, lambda x: math.tanh(float(x)))
    simple("sigmoide", 1, 1, lambda x: 1.0 / (1.0 + math.exp(-float(x))))
    r.registrar("mapear", 2, 2, lambda i, a, f: funcional(i, "mapear", a, f))
    r.registrar("filtrar", 2, 2, lambda i, a, f: funcional(i, "filtrar", a, f))
    r.registrar("reducir", 3, 3, lambda i, a, f, inicial: funcional(i, "reducir", a, f, inicial))
    return r
