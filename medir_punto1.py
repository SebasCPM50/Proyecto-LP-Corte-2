import time
import sys
import os

# Agregamos las carpetas del intérprete
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

from main import ejecutar

print("=================================================================")
print("MEDICIÓN DE RENDIMIENTO: PUNTO 1 (FACTORIAL DE LISTA [1 - n])")
print("=================================================================\n")

archivo_arcanum = "punto1_factorial.arc"
if not os.path.exists(archivo_arcanum):
    archivo_arcanum = os.path.join(os.path.dirname(__file__), "punto1_factorial.arc")

# Medimos el tiempo exacto con el cronómetro de alta resolución de Python
inicio = time.perf_counter()

# Ejecutamos el programa escrito en Arcanum
exito = ejecutar(archivo_arcanum)

fin = time.perf_counter()
tiempo_total = fin - inicio

print("\n-----------------------------------------------------------------")
print(f"[Rendimiento en Python]:")
print(f"  * Tiempo total de ejecución = {tiempo_total:.6f} segundos")
print(f"  * Tiempo en milisegundos   = {tiempo_total * 1000:.2f} ms")
print("-----------------------------------------------------------------")
