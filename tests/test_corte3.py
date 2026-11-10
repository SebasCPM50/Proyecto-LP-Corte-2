"""
Pruebas para los Requisitos de Corte 3 y Entrega Final de Arcanum:
1. Control de flujo: Condicionales (si / sino) y Bucles (mientras, para)
2. Estructuras de datos: Arreglo funcional y Matriz (NumPy artesanal)
3. Machine Learning artesanal: Regresión Lineal, KNN y K-Means
4. Visualización desacoplada: Forja de gráficas a PNG
"""

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from antlr4 import InputStream, CommonTokenStream
from ArcanumLexer import ArcanumLexer
from ArcanumParser import ArcanumParser
from tabla_simbolos import TablaSimbolos
from visitor import ArcanumVisitorEjecutor
from estructuras.arreglo import Arreglo
from estructuras.matriz import Matriz
from ml.regresion import RegresionLineal
from ml.clasificacion import KNNClasificador
from ml.clustering import KMediasClustering
from motor import MotorDatos


def ejecutar_codigo(codigo):
    entrada = InputStream(codigo)
    lexer = ArcanumLexer(entrada)
    tokens = CommonTokenStream(lexer)
    parser = ArcanumParser(tokens)
    arbol = parser.programa()
    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla)
    visitor.visit(arbol)
    return tabla


class TestControlFlujoYColecciones:
    """Pruebas de condicionales si/sino, bucles mientras/para y listas literales."""

    def test_condicional_si_verdadero(self):
        codigo = """
        puntaje = 85;
        si (puntaje >= 60) {
            estado = "Aprobado";
        } sino {
            estado = "Reprobado";
        }
        """
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("estado") == "Aprobado"

    def test_condicional_sino_falso(self):
        codigo = """
        puntaje = 40;
        si (puntaje >= 60) {
            estado = "Aprobado";
        } sino {
            estado = "Reprobado";
        }
        """
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("estado") == "Reprobado"

    def test_bucle_mientras(self):
        codigo = """
        contador = 1;
        acumulador = 0;
        mientras (contador <= 5) {
            acumulador = acumulador + contador;
            contador = contador + 1;
        }
        """
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("contador") == 6
        assert tabla.obtener_valor("acumulador") == 15

    def test_lista_literal_e_indexacion(self):
        codigo = """
        precios = [100, 200, 300];
        primero = precios[0];
        tercero = precios[2];
        """
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("primero") == 100
        assert tabla.obtener_valor("tercero") == 300

    def test_bucle_para(self):
        codigo = """
        numeros = [10, 20, 30];
        acumulador = 0;
        para num en numeros {
            acumulador = acumulador + num;
        }
        """
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("acumulador") == 60


class TestEstructurasNumPyArtesanales:
    """Pruebas de la clase Matriz y Arreglo funcional."""

    def test_matriz_suma_y_transpuesta(self):
        m1 = Matriz([[1, 2], [3, 4]])
        m2 = Matriz([[5, 6], [7, 8]])
        suma = m1.sumar(m2)
        assert suma.filas_datos == [[6.0, 8.0], [10.0, 12.0]]

        trans = m1.transpuesta()
        assert trans.filas_datos == [[1.0, 3.0], [2.0, 4.0]]

    def test_matriz_multiplicacion(self):
        a = Matriz([[1, 2], [3, 4]])
        b = Matriz([[2, 0], [1, 2]])
        prod = a.multiplicar(b)
        # [1*2 + 2*1, 1*0 + 2*2] = [4, 4]
        # [3*2 + 4*1, 3*0 + 4*2] = [10, 8]
        assert prod.filas_datos == [[4.0, 4.0], [10.0, 8.0]]

    def test_arreglo_funcional_map_filter_reduce(self):
        arr = Arreglo([1, 2, 3, 4, 5])
        dobles = arr.mapear(lambda x: x * 2)
        assert dobles.a_lista() == [2, 4, 6, 8, 10]

        pares = arr.filtrar(lambda x: x % 2 == 0)
        assert pares.a_lista() == [2, 4]

        suma = arr.reducir(lambda a, b: a + b, 0)
        assert suma == 15


class TestMachineLearningArtesanal:
    """Pruebas de Regresión Lineal, KNN y K-Means."""

    def test_regresion_lineal_prediccion(self):
        # y = 2*x + 10
        x = [1, 2, 3, 4, 5]
        y = [12, 14, 16, 18, 20]
        reg = RegresionLineal().entrenar(x, y)
        assert abs(reg.pendiente_m - 2.0) < 0.001
        assert abs(reg.intercepto_b - 10.0) < 0.001
        assert abs(reg.r2 - 1.0) < 0.001
        assert abs(reg.predecir(10) - 30.0) < 0.001

    def test_knn_clasificacion(self):
        # Puntos cerca del origen son 'Bajo', puntos lejos son 'Alto'
        datos = [[1.0, 1.0], [1.5, 1.2], [8.0, 9.0], [9.0, 8.5]]
        etiquetas = ["Bajo", "Bajo", "Alto", "Alto"]
        knn = KNNClasificador(k=3).entrenar(datos, etiquetas)
        assert knn.predecir([1.2, 1.1]) == "Bajo"
        assert knn.predecir([8.5, 8.8]) == "Alto"

    def test_kmeans_clustering(self):
        # Dos grupos claramente separados
        datos = [[1.0, 1.0], [1.2, 0.9], [10.0, 10.0], [10.5, 9.8]]
        km = KMediasClustering(k=2, max_iter=10)
        clusters = km.agrupar(datos)
        assert len(clusters) == 4
        # Los dos primeros deben estar en el mismo cluster y los dos últimos en otro
        assert clusters[0] == clusters[1]
        assert clusters[2] == clusters[3]
        assert clusters[0] != clusters[2]


class TestIntegracionDSLCompleto:
    """Pruebas de funciones ML y visualización forjar directamente desde Arcanum."""

    def test_dsl_regresion_y_predecir(self):
        codigo = """
        x_datos = [1, 2, 3, 4];
        y_datos = [2, 4, 6, 8];
        modelo = regresion(x_datos, y_datos);
        prediccion_5 = predecir(modelo, 5);
        """
        tabla = ejecutar_codigo(codigo)
        assert abs(tabla.obtener_valor("prediccion_5") - 10.0) < 0.01

    def test_dsl_knn_clasificador(self):
        codigo = """
        datos = [[1, 1], [2, 1], [8, 8], [9, 9]];
        clases = ["Pequeño", "Pequeño", "Grande", "Grande"];
        modelo_knn = knn(datos, clases, 3);
        resultado = predecir(modelo_knn, [1.5, 1.2]);
        """
        tabla = ejecutar_codigo(codigo)
        assert tabla.obtener_valor("resultado") == "Pequeño"

    def test_dsl_forjar_grafica_png(self, tmp_path):
        ruta_png = os.path.join(str(tmp_path), "test_grafica.png")
        # Usamos ventas.csv para forjar una gráfica de barras
        codigo = f"""
        ventas = invocar desde "csv/ventas.csv";
        resumen = destilar ventas por [ciudad] agregar suma(precio) como total;
        forjar artefacto barras desde resumen con eje_x ciudad, eje_y total, titulo "Prueba", salida "{ruta_png.replace(chr(92), '/')}";
        """
        ejecutar_codigo(codigo)
        assert os.path.exists(ruta_png)
        assert os.path.getsize(ruta_png) > 1000

    def test_dsl_invocar_y_guardar_json(self, tmp_path):
        ruta_json_salida = os.path.join(str(tmp_path), "salida_vuelos.json").replace(chr(92), "/")
        codigo = f"""
        vuelos = invocar desde "datos/vuelos.json";
        vuelos_filtrados = purificar vuelos donde retraso_min > 0;
        preservar vuelos_filtrados en "{ruta_json_salida}";
        """
        tabla = ejecutar_codigo(codigo)
        assert os.path.exists(ruta_json_salida)
        assert os.path.getsize(ruta_json_salida) > 50

    def test_dsl_invocar_vuelos_csv(self):
        codigo = """
        vuelos = invocar desde "datos/vuelos.csv";
        resumen = destilar vuelos por [aerolinea] agregar contar() como total;
        """
        tabla = ejecutar_codigo(codigo)
        pocion = tabla.obtener_pocion("resumen")
        assert len(pocion) > 0
        assert "aerolinea" in pocion.columnas
