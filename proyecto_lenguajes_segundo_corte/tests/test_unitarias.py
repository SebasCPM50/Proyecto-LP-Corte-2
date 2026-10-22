"""
Pruebas unitarias para Arcanum
Acá probamos parte por parte que todo funcione perfecto:
1. La tabla de símbolos (que guarde y busque bien las variables)
2. La Poción artesanal (que filtre, ordene, agrupe y maneje nulos sin usar Pandas)
"""

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from tabla_simbolos import TablaSimbolos
from pocion import Pocion
from motor import MotorDatos
from errores import ErrorSemantico


class TestTablaSimbolos:
    """Acá probamos que la tabla de símbolos guarde variables y detecte fallos de tipo"""

    def test_definir_y_obtener_variable_escalar(self):
        # Probamos guardar un número y recuperarlo
        tabla = TablaSimbolos()
        tabla.definir("tasa", 0.19)
        assert tabla.existe("tasa") is True
        assert tabla.obtener_valor("tasa") == 0.19
        assert tabla.obtener("tasa").tipo == "NUMERO"

    def test_definir_y_obtener_pocion(self):
        # Probamos guardar una tabla completa y verificar que guarde su tipo POCION
        tabla = TablaSimbolos()
        pocion = Pocion(["colA", "colB"], [{"colA": 1, "colB": "x"}, {"colA": 2, "colB": "y"}])
        tabla.definir("mi_pocion", pocion)
        assert tabla.existe("mi_pocion") is True
        assert tabla.obtener("mi_pocion").tipo == "POCION"
        pocion_recuperada = tabla.obtener_pocion("mi_pocion")
        assert len(pocion_recuperada) == 2

    def test_error_variable_inexistente(self):
        # Si pedimos una variable que nadie ha creado debe soltar un error semántico
        tabla = TablaSimbolos()
        with pytest.raises(ErrorSemantico) as excinfo:
            tabla.obtener("variable_fantasma")
        assert "no ha sido declarada" in str(excinfo.value)

    def test_error_columna_inexistente_en_pocion(self):
        # Si pedimos una columna inventada nos tiene que frenar
        tabla = TablaSimbolos()
        pocion = Pocion(["ciudad", "precio"], [{"ciudad": "Bogota", "precio": 100}])
        tabla.definir("ventas", pocion)
        with pytest.raises(ErrorSemantico) as excinfo:
            tabla.verificar_columna("ventas", "columna_no_existe")
        assert "no contiene el ingrediente" in str(excinfo.value)

    def test_error_tipo_no_pocion(self):
        # Si intentamos tratar un simple número como si fuera una tabla debe dar error
        tabla = TablaSimbolos()
        tabla.definir("numero", 42)
        with pytest.raises(ErrorSemantico) as excinfo:
            tabla.obtener_pocion("numero")
        assert "no es una POCIÓN" in str(excinfo.value)


class TestPocionArtesanal:
    """Acá probamos que los métodos de nuestra tabla hecha desde cero funcionen al 100"""

    @pytest.fixture
    def datos_prueba(self):
        # Creamos una tablita pequeña para hacer los tests
        return Pocion(
            ["ciudad", "categoria", "unidades", "precio"],
            [
                {"ciudad": "Bogota", "categoria": "A", "unidades": 2, "precio": 10.0},
                {"ciudad": "Medellin", "categoria": "B", "unidades": 0, "precio": 20.0},
                {"ciudad": "Bogota", "categoria": "A", "unidades": 5, "precio": 15.0},
                {"ciudad": "Cali", "categoria": None, "unidades": 3, "precio": None}
            ]
        )

    def test_recolectar(self, datos_prueba):
        # Probamos seleccionar solo ciudad y unidades
        resultado = datos_prueba.recolectar(["ciudad", "unidades"])
        assert resultado.columnas == ["ciudad", "unidades"]
        assert len(resultado) == 4
        assert "categoria" not in resultado.filas[0]

    def test_purificar(self, datos_prueba):
        # Probamos filtrar las filas donde unidades sea mayor a 1
        resultado = datos_prueba.purificar(lambda fila: fila["unidades"] > 1)
        assert len(resultado) == 3
        assert all(f["unidades"] > 1 for f in resultado.filas)

    def test_ordenar(self, datos_prueba):
        # Probamos ordenar de mayor a menor según las unidades
        resultado = datos_prueba.ordenar("unidades", ascendente=False)
        assert resultado.filas[0]["unidades"] == 5
        assert resultado.filas[-1]["unidades"] == 0

    def test_transmutar(self, datos_prueba):
        # Probamos agregar una columna multiplicando las unidades por 10
        resultado = datos_prueba.transmutar("puntaje", lambda f: f["unidades"] * 10)
        assert "puntaje" in resultado.columnas
        assert resultado.filas[0]["puntaje"] == 20
        # Revisamos que no haya modificado la tabla original
        assert "puntaje" not in datos_prueba.columnas

    def test_sanar_descartar_nulos(self, datos_prueba):
        # La fila de Cali tenía nulos, así que debe desaparecer
        resultado = datos_prueba.sanar_descartar_nulos()
        assert len(resultado) == 3
        assert not any(f["ciudad"] == "Cali" for f in resultado.filas)

    def test_sanar_llenar_nulos(self, datos_prueba):
        # Probamos poner 0.0 donde el precio era nulo
        resultado = datos_prueba.sanar_llenar_nulos("precio", 0.0)
        fila_cali = [f for f in resultado.filas if f["ciudad"] == "Cali"][0]
        assert fila_cali["precio"] == 0.0

    def test_destilar(self, datos_prueba):
        # Probamos agrupar por ciudad y sumar unidades
        agregaciones = [
            {"funcion": "suma", "columna": "unidades", "alias": "total_unidades"},
            {"funcion": "contar", "columna": None, "alias": "cantidad"}
        ]
        resultado = datos_prueba.destilar(["ciudad"], agregaciones)
        assert len(resultado) == 3
        fila_bogota = [f for f in resultado.filas if f["ciudad"] == "Bogota"][0]
        assert fila_bogota["total_unidades"] == 7
        assert fila_bogota["cantidad"] == 2

    def test_muestra_aleatoria(self, datos_prueba):
        # Probamos sacar 2 filas al azar de la tabla
        muestra = datos_prueba.muestra_aleatoria(2)
        assert len(muestra) == 2
        assert muestra.columnas == datos_prueba.columnas

    def test_numero_aleatorio_artesanal(self):
        # Probamos el generador de números al azar sin librerías externas
        from pocion import numero_aleatorio
        num = numero_aleatorio(10, 20)
        assert 10 <= num <= 20
        decimal = numero_aleatorio()
        assert 0.0 <= decimal <= 1.0

