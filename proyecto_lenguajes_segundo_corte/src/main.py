"""
Punto de Entrada Principal — Arcanum (Segundo Corte)
Coordina las etapas del compilador/intérprete:
1. Análisis Léxico (ArcanumLexer)
2. Análisis Sintáctico (ArcanumParser)
3. Análisis Semántico y Ejecución mediante el Patrón Visitor (ArcanumVisitorEjecutor)

Uso:
    python3 main.py <archivo.arc>
    python3 main.py <archivo.arc> --arbol
"""

import sys
import os

# Agregamos la carpeta generated al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from antlr4 import FileStream, CommonTokenStream
from ArcanumLexer import ArcanumLexer
from ArcanumParser import ArcanumParser
from errores import ManejadorErrores, ErrorSemantico
from tabla_simbolos import TablaSimbolos
from visitor import ArcanumVisitorEjecutor


def imprimir_arbol(nodo, parser, sangria=0):
    prefijo = "  " * sangria
    if hasattr(nodo, "getRuleIndex"):
        nombre_regla = parser.ruleNames[nodo.getRuleIndex()]
        print(f"{prefijo}{nombre_regla}")
        for i in range(nodo.getChildCount()):
            imprimir_arbol(nodo.getChild(i), parser, sangria + 1)
    else:
        print(f"{prefijo}'{nodo.getText()}'")


def ejecutar(ruta_archivo, mostrar_arbol=False):
    if not os.path.exists(ruta_archivo):
        print(f"[Error]: El archivo '{ruta_archivo}' no existe")
        return False

    entrada = FileStream(ruta_archivo, encoding="utf-8")

    # 1. ANÁLISIS LÉXICO
    lexer = ArcanumLexer(entrada)
    manejador_lexico = ManejadorErrores()
    lexer.removeErrorListeners()
    lexer.addErrorListener(manejador_lexico)

    tokens = CommonTokenStream(lexer)

    # 2. ANÁLISIS SINTÁCTICO
    parser = ArcanumParser(tokens)
    manejador_sintactico = ManejadorErrores()
    parser.removeErrorListeners()
    parser.addErrorListener(manejador_sintactico)

    arbol = parser.programa()

    if manejador_lexico.hay_errores() or manejador_sintactico.hay_errores():
        print(f"[Falló el análisis] El archivo '{ruta_archivo}' contiene errores sintácticos o léxicos:")
        manejador_lexico.imprimir()
        manejador_sintactico.imprimir()
        return False

    print(f"EJECUTANDO GRIMORIO: {ruta_archivo}")

    if mostrar_arbol:
        print()
        print("[Árbol de Análisis Sintáctico]")
        imprimir_arbol(arbol, parser)
        print()

    # 3. ANÁLISIS SEMÁNTICO Y EJECUCIÓN (PATRÓN VISITOR)
    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla)

    try:
        visitor.visit(arbol)
        print("[Éxito]: El grimorio se ejecutó correctamente sin errores semánticos")
        tabla.imprimir()
        return True
    except ErrorSemantico as e:
        print(f"{e}")
        return False
    except Exception as e:
        print(f"[Error Inesperado durante la ejecución]: {str(e)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo.arc> [--arbol]")
        sys.exit(1)

    argumentos = sys.argv[1:]
    ver_arbol = "--arbol" in argumentos
    rutas = [arg for arg in argumentos if not arg.startswith("--")]

    if not rutas:
        print("Uso: python3 main.py <archivo.arc> [--arbol]")
        sys.exit(1)

    ruta = rutas[0]
    exito = ejecutar(ruta, mostrar_arbol=ver_arbol)
    sys.exit(0 if exito else 1)
