import time
import os
import sys

# Agregamos src y generated al path para medir directamente dentro de Python sin overhead de proceso
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from main import ejecutar

def medir_arcanum(ruta_archivo):
    print(f"=== Midiendo rendimiento de: {ruta_archivo} ===")
    inicio = time.perf_counter()
    exito = ejecutar(ruta_archivo)
    fin = time.perf_counter()
    duracion = fin - inicio
    print(f"\n[Rendimiento]: Tiempo total de ejecución = {duracion:.6f} segundos ({duracion * 1000:.2f} ms)")
    return duracion

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "test_factorial_lista.arc"
    medir_arcanum(archivo)
