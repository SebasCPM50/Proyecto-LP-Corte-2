"""
Perceptrón Multicapa (MLP) artesanal para problemas no lineales (como XOR)
Construido desde cero en Python puro sin dependencias externas (sin PyTorch ni Scikit-learn)
Arquitectura:
  - Capa de entrada (2 neuronas para entradas x1, x2)
  - Capa oculta (2 neuronas con función de activación Sigmoide)
  - Capa de salida (1 neurona con activación Sigmoide)
  - Algoritmo de optimización: Retropropagación (Backpropagation) y Descenso de Gradiente
"""

import math
import random


def _sigmoide(x):
    # Función de activación sigmoide con truncamiento para evitar desbordamiento numérico
    x_acotado = max(min(x, 15.0), -15.0)
    return 1.0 / (1.0 + math.exp(-x_acotado))


def _derivada_sigmoide(s):
    # Derivada analítica s * (1 - s)
    return s * (1.0 - s)


class PerceptronMulticapa:
    """
    Red Neuronal Feedforward de 2 capas para clasificación binaria no lineal.
    Capaz de resolver el problema clásico de XOR.
    """

    def __init__(self, n_entrada=2, n_oculta=2, n_salida=1, tasa_aprendizaje=1.0, epocas=4000):
        self.n_entrada = n_entrada
        self.n_oculta = n_oculta
        self.n_salida = n_salida
        self.tasa = tasa_aprendizaje
        self.epocas = epocas

        # Inicialización de pesos y sesgos con semilla fija para reproducibilidad
        semilla_local = random.Random(42)
        self.w1 = [[semilla_local.uniform(-1.0, 1.0) for _ in range(n_oculta)] for _ in range(n_entrada)]
        self.b1 = [semilla_local.uniform(-1.0, 1.0) for _ in range(n_oculta)]
        self.w2 = [[semilla_local.uniform(-1.0, 1.0) for _ in range(n_salida)] for _ in range(n_oculta)]
        self.b2 = [semilla_local.uniform(-1.0, 1.0) for _ in range(n_salida)]

        self.historial_perdida = []
        self.entrenado = False

    def entrenar(self, X, y):
        """Entrena los pesos de la red usando el algoritmo de backpropagation."""
        X_datos = []
        for fila in X:
            if hasattr(fila, "a_lista"):
                X_datos.append([float(v) for v in fila.a_lista()])
            elif isinstance(fila, (list, tuple)):
                X_datos.append([float(v) for v in fila])
            else:
                X_datos.append([float(fila)])

        y_datos = []
        for fila in y:
            if isinstance(fila, (list, tuple)):
                y_datos.append([float(v) for v in fila])
            elif hasattr(fila, "a_lista"):
                y_datos.append([float(v) for v in fila.a_lista()])
            else:
                y_datos.append([float(fila)])

        N = len(X_datos)
        self.historial_perdida = []

        for epoca in range(self.epocas):
            error_acumulado = 0.0

            for i in range(N):
                xi = X_datos[i]
                target = y_datos[i]

                # 1. Forward Pass (Paso hacia adelante)
                oculta = []
                for j in range(self.n_oculta):
                    z1 = self.b1[j] + sum(xi[k] * self.w1[k][j] for k in range(self.n_entrada))
                    oculta.append(_sigmoide(z1))

                salida = []
                for j in range(self.n_salida):
                    z2 = self.b2[j] + sum(oculta[k] * self.w2[k][j] for k in range(self.n_oculta))
                    salida.append(_sigmoide(z2))

                # Error cuadrático medio
                error_i = sum(0.5 * (target[k] - salida[k]) ** 2 for k in range(self.n_salida))
                error_acumulado += error_i

                # 2. Backward Pass (Retropropagación de errores)
                delta_salida = []
                for k in range(self.n_salida):
                    err = -(target[k] - salida[k])
                    delta_salida.append(err * _derivada_sigmoide(salida[k]))

                delta_oculta = []
                for j in range(self.n_oculta):
                    err_j = sum(delta_salida[k] * self.w2[j][k] for k in range(self.n_salida))
                    delta_oculta.append(err_j * _derivada_sigmoide(oculta[j]))

                # 3. Actualización de pesos y sesgos (Descenso de Gradiente)
                for j in range(self.n_oculta):
                    for k in range(self.n_salida):
                        self.w2[j][k] -= self.tasa * delta_salida[k] * oculta[j]
                for k in range(self.n_salida):
                    self.b2[k] -= self.tasa * delta_salida[k]

                for k in range(self.n_entrada):
                    for j in range(self.n_oculta):
                        self.w1[k][j] -= self.tasa * delta_oculta[j] * xi[k]
                for j in range(self.n_oculta):
                    self.b1[j] -= self.tasa * delta_oculta[j]

            if epoca % 100 == 0 or epoca == self.epocas - 1:
                self.historial_perdida.append(round(error_acumulado / N, 5))

        self.entrenado = True
        return self

    def predecir_probabilidad(self, punto):
        """Retorna la probabilidad continua (0.0 a 1.0) predicha por la neurona de salida."""
        if hasattr(punto, "a_lista"):
            xi = [float(v) for v in punto.a_lista()]
        elif isinstance(punto, (list, tuple)):
            xi = [float(v) for v in punto]
        else:
            xi = [float(punto)]

        oculta = [_sigmoide(self.b1[j] + sum(xi[k] * self.w1[k][j] for k in range(self.n_entrada)))
                  for j in range(self.n_oculta)]
        salida = [_sigmoide(self.b2[j] + sum(oculta[k] * self.w2[k][j] for k in range(self.n_oculta)))
                  for j in range(self.n_salida)]
        return round(salida[0], 4)

    def predecir(self, punto):
        """Retorna la clase binaria predicha (0 o 1) con umbral en 0.5."""
        prob = self.predecir_probabilidad(punto)
        return 1 if prob >= 0.5 else 0

    def a_pocion_perdida(self):
        """Convierte el historial de pérdida a una Poción para graficarla como serie de líneas."""
        from pocion import Pocion
        filas = [{"epoca": idx * 100, "perdida": err} for idx, err in enumerate(self.historial_perdida)]
        return Pocion(["epoca", "perdida"], filas)

    def __repr__(self):
        perdida_final = self.historial_perdida[-1] if self.historial_perdida else "No entrenado"
        return f"<PerceptronMulticapa (MLP XOR): {self.n_entrada}->{self.n_oculta}->{self.n_salida}, Perdida={perdida_final}>"
