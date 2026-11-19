"""Una sola entrada al análisis léxico y sintáctico, sin ejecutar árboles inválidos."""
from antlr4 import InputStream, CommonTokenStream
from ArcanumLexer import ArcanumLexer
from ArcanumParser import ArcanumParser
from errores import ErrorSemantico, ManejadorErrores

def analizar_texto(codigo):
    lexer = ArcanumLexer(InputStream(codigo))
    lexico = ManejadorErrores()
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexico)
    parser = ArcanumParser(CommonTokenStream(lexer))
    sintaxis = ManejadorErrores()
    parser.removeErrorListeners()
    parser.addErrorListener(sintaxis)
    arbol = parser.programa()
    if lexico.hay_errores() or sintaxis.hay_errores():
        lexico.imprimir()
        sintaxis.imprimir()
        raise ErrorSemantico("El programa contiene errores léxicos o sintácticos")
    return arbol

def analizar_archivo(ruta):
    with open(ruta, encoding="utf-8-sig") as archivo:
        return analizar_texto(archivo.read())
