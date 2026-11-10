"""
Módulo de Regresión Lineal (Algoritmo de Predicción para Arcanum)
Implementación 100% matemática y artesanal sin scikit-learn.
Calcula la recta de mejor ajuste y = m*x + b mediante el método de mínimos cuadrados.
"""


class RegresionLineal:
    """
    Modelo supervisado de predicción continua.
    Encuentra la relación lineal entre una variable independiente X y una dependiente Y.
    """

    def __init__(self):
        self.pendiente_m = 0.0
        self.intercepto_b = 0.0
        self.r2 = 0.0
        self.esta_entrenado = False

    def entrenar(self, x, y):
        """
        Calcula m y b usando las ecuaciones normales de mínimos cuadrados:
        m = (N * sum(xy) - sum(x)*sum(y)) / (N * sum(x^2) - (sum(x))^2)
        b = mean(y) - m * mean(x)
        """
        x_vals = [float(v) for v in x]
        y_vals = [float(v) for v in y]
        n = len(x_vals)

        if n < 2 or n != len(y_vals):
            raise ValueError("Se requieren al menos 2 pares de datos (x, y) de igual longitud para entrenar")

        sum_x = sum(x_vals)
        sum_y = sum(y_vals)
        sum_xy = sum(xi * yi for xi, yi in zip(x_vals, y_vals))
        sum_x2 = sum(xi ** 2 for xi in x_vals)

        denominador = (n * sum_x2) - (sum_x ** 2)
        if denominador == 0:
            # Línea vertical sin variación en X
            self.pendiente_m = 0.0
            self.intercepto_b = sum_y / n
        else:
            self.pendiente_m = ((n * sum_xy) - (sum_x * sum_y)) / denominador
            self.intercepto_b = (sum_y - (self.pendiente_m * sum_x)) / n

        # Cálculo del coeficiente de determinación R^2
        media_y = sum_y / n
        ss_tot = sum((yi - media_y) ** 2 for yi in y_vals)
        ss_res = sum((yi - (self.pendiente_m * xi + self.intercepto_b)) ** 2 for xi, yi in zip(x_vals, y_vals))
        self.r2 = (1.0 - (ss_res / ss_tot)) if ss_tot != 0 else 1.0

        self.esta_entrenado = True
        return self

    def predecir(self, nuevo_x):
        """Predice el valor de y para un nuevo valor escalar de x."""
        if not self.esta_entrenado:
            raise RuntimeError("El modelo de regresión no ha sido entrenado todavía")
        return round(self.pendiente_m * float(nuevo_x) + self.intercepto_b, 4)

    def predecir_lote(self, lista_x):
        """Predice para una lista de valores de x."""
        return [self.predecir(x) for x in lista_x]

    def resumen(self):
        """Retorna un resumen legible de los parámetros aprendidos."""
        signo = "+" if self.intercepto_b >= 0 else "-"
        return (
            f"Regresión Lineal: y = {self.pendiente_m:.4f} * x {signo} {abs(self.intercepto_b):.4f} "
            f"(R² = {self.r2:.4f})"
        )

    def __repr__(self):
        if not self.esta_entrenado:
            return "<RegresionLineal: no entrenada>"
        return f"<RegresionLineal: y = {self.pendiente_m:.2f}x + {self.intercepto_b:.2f}, R²={self.r2:.2f}>"
