"""
Pruebas de integración para Arcanum
Acá corremos los programas completos de punta a punta y revisamos que
los archivos CSV que se guardan en la carpeta salidas/ queden bien escritos
"""

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from main import ejecutar
from pocion import Pocion


class TestIntegracionProgramas:
    """Acá probamos que los ejemplos reales de Arcanum corran completos sin fallar"""

    def test_ejecutar_valido_asignaciones(self):
        # Corre el ejemplo de variables básicas
        ruta = os.path.join("tests", "fixtures", "valido_asignaciones.arc")
        if not os.path.exists(ruta):
            ruta = os.path.join("examples", "valido_asignaciones.arc")
        assert ejecutar(ruta) is True

    def test_ejecutar_valido_completo(self):
        # Corre el ejemplo con todas las operaciones
        ruta = os.path.join("tests", "fixtures", "valido_completo.arc")
        if not os.path.exists(ruta):
            ruta = os.path.join("examples", "valido_completo.arc")
        assert ejecutar(ruta) is True

    def test_ejecutar_programa1_ventas_y_verificar_csv(self):
        # Corre el caso de ventas y revisa que el archivo CSV se haya guardado
        ruta = os.path.join("examples", "ejemplo1_analisis_ventas.arc")
        assert ejecutar(ruta) is True

        archivo_salida = os.path.join("salidas", "resumen_ventas_ciudad.csv")
        assert os.path.exists(archivo_salida) is True

        # Leemos el archivo generado con nuestra clase artesanal Pocion
        pocion_exportada = Pocion.desde_csv(archivo_salida)
        assert len(pocion_exportada) > 0
        assert "ciudad" in pocion_exportada.columnas
        assert "ingreso_total" in pocion_exportada.columnas

    def test_ejecutar_ejemplo8_control_y_listas(self):
        ruta = os.path.join("examples", "ejemplo8_control_y_listas.arc")
        assert ejecutar(ruta) is True

    def test_ejecutar_ejemplo7_casos_profesor(self):
        ruta = os.path.join("examples", "ejemplo7_casos_profesor.arc")
        assert ejecutar(ruta) is True
