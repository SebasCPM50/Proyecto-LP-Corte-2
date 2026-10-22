"""
Pruebas semánticas para Arcanum
Acá probamos que el compilador se dé cuenta cuando alguien escribe algo ilógico:
1. Usar variables que no existen
2. Pedir columnas que no están en el CSV
3. Intentar operar tipos incompatibles
4. Dividir por cero
5. Cargar compendios y recetas propias
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
    # Función de ayuda para ejecutar un pedazo de código en texto directo
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
        raise SyntaxError("Error sintáctico o léxico en el código de prueba")

    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla)
    visitor.visit(arbol)
    return tabla


class TestValidacionesSemanticas:
    """Acá probamos que salten los errores semánticos correctos cuando algo esté mal escrito"""

    def test_error_variable_no_declarada(self):
        # Si sumamos una variable que no existe debe dar error
        codigo = 'x = 10; total = x + variable_inexistente;'
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "no ha sido declarada" in str(excinfo.value)

    def test_error_columna_inexistente(self):
        # Si recolectamos una columna que no está en el CSV debe avisar
        codigo = '''
        datos = invocar desde "csv/ventas.csv";
        filtrado = recolectar [columna_falsa] de datos;
        '''
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "no contiene el ingrediente" in str(excinfo.value)

    def test_error_tipo_incompatible_en_operacion(self):
        # Si intentamos recolectar columnas de un número flotante debe saltar error
        codigo = '''
        descuento = 0.10;
        resultado = recolectar [ciudad] de descuento;
        '''
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "no es una POCIÓN" in str(excinfo.value)

    def test_error_division_por_cero(self):
        # No se puede dividir entre cero
        codigo = 'resultado = 100 / 0;'
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "División por cero" in str(excinfo.value)

    def test_error_archivo_csv_no_encontrado(self):
        # Si el archivo no existe en disco debe avisar amablemente
        codigo = 'datos = invocar desde "csv/archivo_que_no_existe_jamas.csv";'
        with pytest.raises(ErrorSemantico) as excinfo:
            ejecutar_codigo(codigo)
        assert "No se pudo invocar el archivo" in str(excinfo.value)

    def test_definicion_y_llamada_receta_local(self):
        # Probamos definir una función y llamarla
        codigo = '''
        receta duplicar(valor) {
            devolver valor * 2;
        }
        resultado = duplicar(25);
        '''
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("resultado") == 50

    def test_usar_compendio_propio(self):
        # Probamos cargar una librería propia de compendios y llamar a su receta
        codigo = '''
        usar compendio matematicas;
        impuesto = matematicas.calcular_iva(200, 0.19);
        '''
        tabla = ejecutar_codigo(codigo)
        assert abs(tabla.obtener_valor("impuesto") - 38.0) < 0.001

    def test_funcion_random_integrada(self):
        # Probamos llamar a la función random nativa del lenguaje
        codigo = '''
        dado = random(1, 6);
        decimal = random();
        '''
        tabla = ejecutar_codigo(codigo)
        assert 1 <= tabla.obtener_valor("dado") <= 6
        assert 0.0 <= tabla.obtener_valor("decimal") <= 1.0

    def test_funcion_random_compendio(self):
        # Probamos llamar a la receta random del compendio de matematicas
        codigo = '''
        usar compendio matematicas;
        aleatorio = matematicas.random(42, 10, 50);
        '''
        tabla = ejecutar_codigo(codigo)
        assert 10 <= tabla.obtener_valor("aleatorio") <= 50

