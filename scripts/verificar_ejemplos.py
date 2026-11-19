"""Ejecuta todos los ejemplos y comprueba sus códigos de salida."""
from pathlib import Path
import subprocess
import sys

raiz = Path(__file__).resolve().parents[1]
fallos = []
for archivo in sorted((raiz / "examples").glob("*.arc")):
    debe_fallar = archivo.name.startswith("invalido_")
    try:
        proceso = subprocess.run([sys.executable, "src/main.py", str(archivo)],
                                 cwd=raiz, capture_output=True, text=True, timeout=60)
        correcto = (proceso.returncode == 1) if debe_fallar else (proceso.returncode == 0)
        print(f"{'OK' if correcto else 'FALLO'} {archivo.name}")
        if not correcto:
            fallos.append(archivo.name)
            print(proceso.stdout, proceso.stderr)
    except subprocess.TimeoutExpired:
        fallos.append(archivo.name)
        print(f"FALLO {archivo.name}: excedió 60 segundos")
print(f"\n{len(list((raiz / 'examples').glob('*.arc')))} ejemplos revisados; {len(fallos)} fallos inesperados")
sys.exit(bool(fallos))
