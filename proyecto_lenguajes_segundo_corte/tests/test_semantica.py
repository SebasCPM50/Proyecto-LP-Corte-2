"""
Pruebas Semánticas — Arcanum
============================
Verifica que el analizador semántico detecte y reporte adecuadamente:
1. Variables no declaradas
2. Columnas inexistentes en una poción
3. Operaciones entre tipos incompatibles
4. División por cero
5. Sistema de compendios y recetas (librerías propias)
"""

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from antlr4 import InputStream, CommonTokenStream
from ArcanumLexer import ArcanumLexer
from ArcanumParser import ArcanumParser
from errores import ErrorSemantico, ManejadorErrores
from tabla_simbolos import TablaSimbolos
from visitor import ArcanumVisitorEjecutor


def ejecutar_codigo(codigo_fuente):
    """Función auxiliar para parsear y ejecutar una cadena de código Arcanum."""
    entrada = InputStream(codigo_fuente)
    lexer = ArcanumLexer(entrada)
    manejador_lex = ManejadorErrores()
    lexer.removeErrorListeners()
    lexer.addErrorListener(manejador_lex)

    tokens = CommonTokenStream(lexer)
    parser = ArcanumParser(tokens)
    manejador_sin = ManejadorErrores()
    parser.removeErrorListeners()
    parser.addErrorListener(manejador_sin)

    arbol = parser.programa()
    if manejador_lex.hay_errores() or manejador_sin.hay_errores():
        raise SyntaxError("Error sintáctico o léxico en el código de prueba.")

    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla)
    visitor.visit(arbol)
    return tabla


class TestValidacionesSemanticas:

    def test_error_variable_no_declarada(self):
        codigo = 'x = 10; total = x + variable_inexistente;'
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "no ha sido declarada" in str(excinfo.value)

    def test_error_columna_inexistente(self):
        codigo = '''
        datos = invocar desde "csv/ventas.csv";
        filtrado = recolectar [columna_falsa] de datos;
        '''
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "no contiene el ingrediente" in str(excinfo.value)

    def test_error_tipo_incompatible_en_operacion(self):
        codigo = '''
        descuento = 0.10;
        resultado = recolectar [ciudad] de descuento;
        '''
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "no es una POCIÓN" in str(excinfo.value)

    def test_error_division_por_cero(self):
        codigo = 'resultado = 100 / 0;'
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "División por cero" in str(excinfo.value)

    def test_error_archivo_csv_no_encontrado(self):
        codigo = 'datos = invocar desde "csv/archivo_que_no_existe_jamas.csv";'
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "No se pudo invocar el archivo" in str(excinfo.value)

    def test_definicion_y_llamada_receta_local(self):
        codigo = '''
        receta duplicar(valor) {
            devolver valor * 2;
        }
        resultado = duplicar(25);
        '''
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("resultado") == 50

    def test_usar_compendio_propio(self):
        codigo = '''
        usar compendio matematicas;
        impuesto = matematicas.calcular_iva(200, 0.19);
        '''
        tabla = ejecutar_codigo(codigo)
        assert abs(tabla.obtener_valor("impuesto") - 38.0) < 0.001
