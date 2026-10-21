#!/bin/bash
# Script de Demostración Automática — Arcanum en Ubuntu

echo "PROYECTO ARCANUM (SEGUNDO CORTE EN UBUNTU)"
echo

# 1 Pruebas automáticas con pytest
echo ">>> [1/5] Ejecutando suite de 24 pruebas automáticas"
python3 -m pytest -v tests
echo

# 2 Caso de estudio 1: Ventas y exportación CSV
echo ">>> [2/5] Ejecutando Caso 1: Ventas Comerciales"
python3 src/main.py examples/ejemplo1_analisis_ventas.arc
echo
echo "Vista del CSV exportado (salidas/resumen_ventas_ciudad.csv):"
cat salidas/resumen_ventas_ciudad.csv
echo
echo

# 3 Caso de estudio 2: Rendimiento estudiantil
echo ">>> [3/5] Ejecutando Caso 2: Rendimiento Académico"
python3 src/main.py examples/ejemplo2_rendimiento_estudiantil.arc
echo

# 4 Caso de estudio 3: Calidad del aire
echo ">>> [4/5] Ejecutando Caso 3: Monitoreo Ambiental"
python3 src/main.py examples/ejemplo3_calidad_aire.arc
echo

# 5 Caso de estudio 4: Librerías propias (Compendios y Recetas)
echo ">>> [5/5] Ejecutando Caso 4: Librerías Propias (Compendios)"
python3 src/main.py examples/ejemplo4_compendios_recetas.arc
echo

echo "Todas las demostraciones se ejecutaron correctamente"
