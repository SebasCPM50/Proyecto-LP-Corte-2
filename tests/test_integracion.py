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
        ruta = os.path.join("examples", "valido_asignaciones.arc")
        assert ejecutar(ruta) is True

    def test_ejecutar_valido_completo(self):
        # Corre el ejemplo con todas las operaciones
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

    def test_ejecutar_programa2_estudiantes_y_verificar_csv(self):
        # Corre el caso de estudiantes y revisa el CSV exportado
        ruta = os.path.join("examples", "ejemplo2_rendimiento_estudiantil.arc")
        assert ejecutar(ruta) is True

        archivo_salida = os.path.join("salidas", "resumen_estudiantes.csv")
        assert os.path.exists(archivo_salida) is True

        pocion_exportada = Pocion.desde_csv(archivo_salida)
        assert len(pocion_exportada) > 0
        assert "carrera" in pocion_exportada.columnas
        assert "promedio_general" in pocion_exportada.columnas

    def test_ejecutar_programa3_calidad_aire_y_verificar_csv(self):
        # Corre el caso ambiental y revisa las columnas exportadas
        ruta = os.path.join("examples", "ejemplo3_calidad_aire.arc")
        assert ejecutar(ruta) is True

        archivo_salida = os.path.join("salidas", "resumen_calidad_aire.csv")
        assert os.path.exists(archivo_salida) is True

        pocion_exportada = Pocion.desde_csv(archivo_salida)
        assert len(pocion_exportada) > 0
        assert "estacion" in pocion_exportada.columnas
        assert "pm25_promedio" in pocion_exportada.columnas
