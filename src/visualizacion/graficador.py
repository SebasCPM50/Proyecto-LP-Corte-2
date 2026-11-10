"""
Motor de Visualización Gráfica para Arcanum (Nuestra capa sobre Matplotlib)
Genera representaciones visuales a partir de datos tabulares (Pociones)
y las exporta directamente a imágenes PNG de alta resolución.
Soporta: barras, líneas, dispersión, histogramas y diagramas de caja.
"""

import os
import matplotlib
matplotlib.use('Agg') # Modo sin interfaz gráfica para generación limpia en consola/servidor
import matplotlib.pyplot as plt


class GraficadorArcanum:
    """
    Fachada desacoplada de visualización.
    Extrae los datos de la Poción y genera gráficas exportables a PNG.
    """

    PALETA_COLORES = {
        "barras": "#2B6CB0",     # Azul medio elegante
        "lineas": "#319795",     # Verde azulado
        "dispersion": "#DD6B20", # Naranja
        "histograma": "#805AD5", # Púrpura
        "caja": "#4A5568"        # Gris pizarra
    }

    @classmethod
    def forjar(cls, tipo, pocion, eje_x=None, eje_y=None, titulo=None, ruta_salida=None, color=None):
        tipo_normalizado = tipo.lower().strip()
        if not ruta_salida:
            ruta_salida = os.path.join("salidas", f"grafica_{tipo_normalizado}.png")

        # Aseguramos que la carpeta de destino exista
        directorio = os.path.dirname(ruta_salida)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        color_final = color if color else cls.PALETA_COLORES.get(tipo_normalizado, "#2B6CB0")
        titulo_final = titulo if titulo else f"Gráfica de {tipo_normalizado.capitalize()}"

        plt.figure(figsize=(9, 5))
        plt.grid(True, linestyle="--", alpha=0.5, zorder=1)

        # 1. Gráfica de Barras
        if tipo_normalizado in ["barras", "barra", "bar"]:
            valores_x = [str(f.get(eje_x, "")) for f in pocion.filas]
            valores_y = [float(f.get(eje_y, 0.0)) for f in pocion.filas]
            plt.bar(valores_x, valores_y, color=color_final, edgecolor="black", alpha=0.85, zorder=2)
            plt.xlabel(eje_x if eje_x else "Categoría")
            plt.ylabel(eje_y if eje_y else "Valor")
            plt.xticks(rotation=25, ha="right")

        # 2. Gráfica de Líneas
        elif tipo_normalizado in ["lineas", "linea", "line"]:
            valores_x = [str(f.get(eje_x, "")) for f in pocion.filas]
            valores_y = [float(f.get(eje_y, 0.0)) for f in pocion.filas]
            plt.plot(valores_x, valores_y, marker="o", color=color_final, linewidth=2, zorder=3)
            plt.xlabel(eje_x if eje_x else "X")
            plt.ylabel(eje_y if eje_y else "Y")
            plt.xticks(rotation=25, ha="right")

        # 3. Gráfica de Dispersión (Scatter Plot)
        elif tipo_normalizado in ["dispersion", "scatter", "puntos"]:
            valores_x = [float(f.get(eje_x, 0.0)) for f in pocion.filas]
            valores_y = [float(f.get(eje_y, 0.0)) for f in pocion.filas]
            plt.scatter(valores_x, valores_y, color=color_final, edgecolor="black", s=70, alpha=0.85, zorder=3)
            plt.xlabel(eje_x if eje_x else "Variable X")
            plt.ylabel(eje_y if eje_y else "Variable Y")

        # 4. Histograma
        elif tipo_normalizado in ["histograma", "hist"]:
            col_target = eje_x if eje_x else (eje_y if eje_y else pocion.columnas[0])
            valores = [float(f.get(col_target, 0.0)) for f in pocion.filas if f.get(col_target) is not None]
            plt.hist(valores, bins=8, color=color_final, edgecolor="black", alpha=0.85, zorder=2)
            plt.xlabel(col_target)
            plt.ylabel("Frecuencia")

        # 5. Diagrama de Caja (Boxplot)
        elif tipo_normalizado in ["caja", "boxplot"]:
            col_target = eje_y if eje_y else (eje_x if eje_x else pocion.columnas[0])
            valores = [float(f.get(col_target, 0.0)) for f in pocion.filas if f.get(col_target) is not None]
            plt.boxplot(valores, patch_artist=True, boxprops=dict(facecolor=color_final, alpha=0.7))
            plt.ylabel(col_target)

        else:
            plt.close()
            raise ValueError(f"Tipo de gráfica no soportado: '{tipo}'. Tipos válidos: barras, lineas, dispersion, histograma, caja")

        plt.title(titulo_final, fontsize=13, fontweight="bold", pad=12)
        plt.tight_layout()
        plt.savefig(ruta_salida, dpi=150)
        plt.close()

        print(f"[Artefacto Forjado]: Gráfica de {tipo_normalizado} exportada exitosamente a '{ruta_salida}'")
        return ruta_salida
