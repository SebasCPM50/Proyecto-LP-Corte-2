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

# Agregamos las carpetas src y generated para poder importar las clases modulares
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from analizador import analizar_archivo
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


def ejecutar(ruta_archivo, mostrar_arbol=False, max_iteraciones=10000):
    """
    Acá orquestamos todo el proceso desde abrir el archivo hasta ejecutar el código
    """
    # Verificamos primero que el archivo sí exista en disco
    if not os.path.exists(ruta_archivo):
        print(f"[Error]: El archivo '{ruta_archivo}' no existe")
        return False

    try:
        arbol = analizar_archivo(ruta_archivo)
    except (ErrorSemantico, OSError, UnicodeError) as error:
        print(error)
        return False
    parser = ArcanumParser

    print(f"EJECUTANDO GRIMORIO: {ruta_archivo}")

    # Si pidieron ver el árbol de derivación lo mostramos acá
    if mostrar_arbol:
        print()
        print("[Árbol de Análisis Sintáctico]")
        imprimir_arbol(arbol, parser)
        print()

    # Paso 3: Análisis Semántico y Ejecución con nuestro Visitor
    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla, max_iteraciones)

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


def cli():
    import argparse
    parser = argparse.ArgumentParser(description="Ejecuta programas del lenguaje Arcanum")
    parser.add_argument("archivo", help="Ruta del programa .arc")
    parser.add_argument("--arbol", action="store_true", help="Muestra el árbol sintáctico")
    parser.add_argument("--max-iteraciones", type=int, default=10000,
                        help="Límite por bucle mientras (por defecto 10000)")
    args = parser.parse_args()
    if args.max_iteraciones <= 0:
        parser.error("--max-iteraciones debe ser positivo")
    return 0 if ejecutar(args.archivo, args.arbol, args.max_iteraciones) else 1


if __name__ == "__main__":
    sys.exit(cli())
