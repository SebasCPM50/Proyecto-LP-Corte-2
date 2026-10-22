"""
Punto de entrada principal para Arcanum
Acá conectamos todo el flujo del compilador:
1. El analizador léxico que separa el texto en palabras clave (tokens)
2. El analizador sintáctico que revisa la gramática
3. El Visitor que recorre el árbol y ejecuta las operaciones usando nuestra Poción artesanal

Cómo se corre:
  python3 main.py <archivo.arc>
  python3 main.py <archivo.arc> --arbol
"""

import sys
import os

# Agregamos la carpeta generated para poder importar las clases de ANTLR
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from antlr4 import FileStream, CommonTokenStream
from ArcanumLexer import ArcanumLexer
from ArcanumParser import ArcanumParser
from errores import ManejadorErrores, ErrorSemantico
from tabla_simbolos import TablaSimbolos
from visitor import ArcanumVisitorEjecutor


def imprimir_arbol(nodo, parser, sangria=0):
    """
    Función recursiva para pintar el árbol sintáctico en la terminal con sangrías
    si el usuario le pasa la opción --arbol
    """
    prefijo = "  " * sangria
    # Si es una regla de la gramática mostramos su nombre
    if hasattr(nodo, "getRuleIndex"):
        nombre_regla = parser.ruleNames[nodo.getRuleIndex()]
        print(f"{prefijo}{nombre_regla}")
        for i in range(nodo.getChildCount()):
            imprimir_arbol(nodo.getChild(i), parser, sangria + 1)
    else:
        # Si es una hoja terminal mostramos el texto exacto
        print(f"{prefijo}'{nodo.getText()}'")


def ejecutar(ruta_archivo, mostrar_arbol=False):
    """
    Acá orquestamos todo el proceso desde abrir el archivo hasta ejecutar el código
    """
    # Verificamos primero que el archivo sí exista en disco
    if not os.path.exists(ruta_archivo):
        print(f"[Error]: El archivo '{ruta_archivo}' no existe")
        return False

    # Leemos el archivo en texto UTF-8 con ANTLR
    entrada = FileStream(ruta_archivo, encoding="utf-8")

    # Paso 1: Análisis Léxico (dividimos el texto en tokens)
    lexer = ArcanumLexer(entrada)
    manejador_lexico = ManejadorErrores()
    lexer.removeErrorListeners()
    lexer.addErrorListener(manejador_lexico)

    tokens = CommonTokenStream(lexer)

    # Paso 2: Análisis Sintáctico (construimos el árbol siguiendo la gramática)
    parser = ArcanumParser(tokens)
    manejador_sintactico = ManejadorErrores()
    parser.removeErrorListeners()
    parser.addErrorListener(manejador_sintactico)

    arbol = parser.programa()

    # Si hubo algún fallo de sintaxis o palabras mal escritas paramos de una vez
    if manejador_lexico.hay_errores() or manejador_sintactico.hay_errores():
        print(f"[Falló el análisis] El archivo '{ruta_archivo}' contiene errores sintácticos o léxicos:")
        manejador_lexico.imprimir()
        manejador_sintactico.imprimir()
        return False

    print(f"EJECUTANDO GRIMORIO: {ruta_archivo}")

    # Si pidieron ver el árbol de derivación lo mostramos acá
    if mostrar_arbol:
        print()
        print("[Árbol de Análisis Sintáctico]")
        imprimir_arbol(arbol, parser)
        print()

    # Paso 3: Análisis Semántico y Ejecución con nuestro Visitor
    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla)

    try:
        # Recorremos el árbol y ejecutamos cada hechizo
        visitor.visit(arbol)
        print("[Éxito]: El grimorio se ejecutó correctamente sin errores semánticos")
        tabla.imprimir()
        return True
    except ErrorSemantico as e:
        # Si hay un error de variables o tipos lo mostramos claro
        print(f"{e}")
        return False
    except Exception as e:
        # Si llega a pasar algo no previsto lo atrapamos acá
        print(f"[Error Inesperado durante la ejecución]: {str(e)}")
        return False


if __name__ == "__main__":
    # Revisamos que nos hayan pasado el nombre del archivo por consola
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
