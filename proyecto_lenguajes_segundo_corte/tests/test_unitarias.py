"""
Pruebas Unitarias — Arcanum
===========================
Verifica el funcionamiento aislado de los componentes fundamentales:
1. Tabla de Símbolos
2. Estructura de Datos Artesanal Pocion (100% Pura, Sin Pandas)
3. Motor de Datos y Compendios
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
    """Pruebas unitarias sobre la gestión de símbolos y memoria."""

    def test_definir_y_obtener_variable_escalar(self):
        tabla = TablaSimbolos()
        tabla.definir("tasa", 0.19)
        assert tabla.existe("tasa") is True
        assert tabla.obtener_valor("tasa") == 0.19
        assert tabla.obtener("tasa").tipo == "NUMERO"

    def test_definir_y_obtener_pocion(self):
        tabla = TablaSimbolos()
        pocion = Pocion(["colA", "colB"], [{"colA": 1, "colB": "x"}, {"colA": 2, "colB": "y"}])
        tabla.definir("mi_pocion", pocion)
        assert tabla.existe("mi_pocion") is True
        assert tabla.obtener("mi_pocion").tipo == "POCION"
        pocion_recuperada = tabla.obtener_pocion("mi_pocion")
        assert len(pocion_recuperada) == 2

    def test_error_variable_inexistente(self):
        tabla = TablaSimbolos()
        with pytest.raises(ErrorSemantico) as excinfo:
            tabla.obtener("variable_fantasma")
        assert "no ha sido declarada" in str(excinfo.value)

    def test_error_columna_inexistente_en_pocion(self):
        tabla = TablaSimbolos()
        pocion = Pocion(["ciudad", "precio"], [{"ciudad": "Bogota", "precio": 100}])
        tabla.definir("ventas", pocion)
        with pytest.raises(ErrorSemantico) as excinfo:
            tabla.verificar_columna("ventas", "columna_no_existe")
        assert "no contiene el ingrediente" in str(excinfo.value)

    def test_error_tipo_no_pocion(self):
        tabla = TablaSimbolos()
        tabla.definir("numero", 42)
        with pytest.raises(ErrorSemantico) as excinfo:
            tabla.obtener_pocion("numero")
        assert "no es una POCIÓN" in str(excinfo.value)


class TestPocionArtesanal:
    """Pruebas sobre las transformaciones tabulares hechas 100% a mano sin pandas."""

    @pytest.fixture
    def datos_prueba(self):
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
        resultado = datos_prueba.recolectar(["ciudad", "unidades"])
        assert resultado.columnas == ["ciudad", "unidades"]
        assert len(resultado) == 4
        assert "categoria" not in resultado.filas[0]

    def test_purificar(self, datos_prueba):
        # Filtrar donde unidades > 1
        resultado = datos_prueba.purificar(lambda fila: fila["unidades"] > 1)
        assert len(resultado) == 3
        assert all(f["unidades"] > 1 for f in resultado.filas)

    def test_ordenar(self, datos_prueba):
        resultado = datos_prueba.ordenar("unidades", ascendente=False)
        assert resultado.filas[0]["unidades"] == 5
        assert resultado.filas[-1]["unidades"] == 0

    def test_transmutar(self, datos_prueba):
        resultado = datos_prueba.transmutar("puntaje", lambda f: f["unidades"] * 10)
        assert "puntaje" in resultado.columnas
        assert resultado.filas[0]["puntaje"] == 20
        # Inmutabilidad: el original no debe tener la nueva columna
        assert "puntaje" not in datos_prueba.columnas

    def test_sanar_descartar_nulos(self, datos_prueba):
        resultado = datos_prueba.sanar_descartar_nulos()
        assert len(resultado) == 3
        # La fila de Cali tenía nulos, no debe estar
        assert not any(f["ciudad"] == "Cali" for f in resultado.filas)

    def test_sanar_llenar_nulos(self, datos_prueba):
        resultado = datos_prueba.sanar_llenar_nulos("precio", 0.0)
        fila_cali = [f for f in resultado.filas if f["ciudad"] == "Cali"][0]
        assert fila_cali["precio"] == 0.0

    def test_destilar(self, datos_prueba):
        agregaciones = [
            {"funcion": "suma", "columna": "unidades", "alias": "total_unidades"},
            {"funcion": "contar", "columna": None, "alias": "cantidad"}
        ]
        resultado = datos_prueba.destilar(["ciudad"], agregaciones)
        assert len(resultado) == 3  # Bogota, Cali, Medellin
        fila_bogota = [f for f in resultado.filas if f["ciudad"] == "Bogota"][0]
        assert fila_bogota["total_unidades"] == 7
        assert fila_bogota["cantidad"] == 2
