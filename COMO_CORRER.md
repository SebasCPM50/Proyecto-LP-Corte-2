# Guía de Ejecución y Pruebas de Arcanum

Este documento explica de forma detallada cómo instalar dependencias, ejecutar cada uno de los **9 programas de ejemplo** y verificar las pruebas unitarias del compilador/intérprete **Arcanum**.

---

## 1. Requisitos e Instalación

Necesitas **Python 3.10 o superior**. El repositorio ya incluye el lexer y parser generados por ANTLR en `generated/`, por lo que **no necesitas tener Java instalado** para ejecutar Arcanum.

### Opción A: Instalación con Entorno Virtual (Recomendada)

#### En Linux o macOS:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

#### En Windows (PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Opción B: Instalación Global Directa (Sin Entorno Virtual)

Si estás trabajando en una máquina virtual de Ubuntu o en tu entorno global:
```bash
pip3 install antlr4-python3-runtime==4.13.2 pytest matplotlib openpyxl --break-system-packages
```

En Windows:
```powershell
pip install antlr4-python3-runtime==4.13.2 pytest matplotlib openpyxl
```

> **IMPORTANTE**: Ejecuta siempre todos los comandos desde la **carpeta raíz del proyecto** (la carpeta donde se encuentran `src/`, `examples/` y `requirements.txt`). Nunca ejecutes comandos desde dentro de `src/`.

---

## 2. Verificación Global del Sistema

Para verificar que todo el compilador y los módulos de Machine Learning funcionan al 100%:

### A. Correr las 81 pruebas automatizadas (pytest)
```bash
# Con entorno virtual:
.venv/bin/python -m pytest -q

# O globalmente:
pytest -q
```
*Resultado esperado*: `81 passed in ~2s`.

### B. Correr el verificador de los 9 ejemplos
```bash
# Con entorno virtual:
.venv/bin/python scripts/verificar_ejemplos.py

# O globalmente:
python3 scripts/verificar_ejemplos.py
```
*Resultado esperado*: `9 ejemplos revisados; 0 fallos inesperados`.

---

## 3. Catálogo de los 9 Ejemplos Oficiales

Para ejecutar cualquier ejemplo, usa la sintaxis:
```bash
python3 src/main.py examples/<nombre_del_ejemplo>.arc
```

| Número | Archivo | Qué demuestra | Salida generada |
|---|---|---|---|
| **1** | `examples/ejemplo1_analisis_ventas.arc` | **Pipeline ETL en CSV**: Carga boletos aéreos, limpia nulos (`sanar`), purifica compras inválidas, calcula totales (`transmutar`), agrupa por destino (`destilar`) y exporta a CSV. | `salidas/resumen_ventas_ciudad.csv` |
| **2** | `examples/ejemplo2_rendimiento_estudiantil.arc` | **Filtros Académicos en CSV**: Descarta nulos, exige asistencia $\ge 75\%$, calcula promedios y agrupa por carrera universitaria. | `salidas/resumen_estudiantes.csv` |
| **3** | `examples/ejemplo3_calidad_aire.arc` | **Imputación Ambiental en CSV**: Rellena valores faltantes de PM10 con 50, filtra lecturas positivas y resume métricas por estación de monitoreo. | `salidas/resumen_calidad_aire.csv` |
| **4** | `examples/ejemplo4_compendios_recetas.arc` | **Compendios y Librerías Modulares**: Uso de `usar compendio matematicas;` y `usar compendio estadistica;`, invocando recetas externas y números pseudoaleatorios. | `salidas/ventas_con_librerias_propias.csv` |
| **5** | `examples/ejemplo5_caso_estudio_final.arc` | **Caso Integral de Machine Learning y Gráficos**: Pipeline completo con Regresión Lineal, KNN, K-Means, matrices y 4 gráficos estadísticos PNG. | 4 imágenes `.png` y resumen CSV/JSON |
| **6** | `examples/ejemplo6_analisis_vuelos_json.arc` | **Analítica Multiformato JSON**: Lectura nativa de archivos JSON (`datos/vuelos.json`), cálculo de retrasos por aerolínea y gráfico de barras PNG. | `salidas/5_grafica_retraso_aerolineas.png` y JSON exportado |
| **7** | `examples/ejemplo7_casos_profesor.arc` | **Los 5 Ejercicios del Tablero**: Factorial (5 a 100), Sigmoide real calculada, Perceptrón XOR, EDA de Excel (`Data.xlsx`) y filtro funcional de Primos. | `salidas/6_grafica_sigmoide_tendencia.png`, `8_perdida_xor.png`, CSVs |
| **8** | `examples/ejemplo8_control_y_listas.arc` | **Fundamentos de Programación**: Asignación de variables, condicionales `si/sino`, bucle `mientras` con acumulador y manejo de listas (`Arreglo`). | Impresión clara en consola |
| **9** | `examples/ejemplo9_estructuras_funcionales.arc` | **Programación Funcional y Matrices**: Transformación con `mapear`, `filtrar` y `reducir`, y álgebra lineal (suma y producto de matrices $2 \times 2$). | Impresión de colecciones y matrices |

---

## 4. Parámetros Avanzados de la Terminal

### Inspeccionar el Árbol de Análisis Sintáctico (CST/AST de ANTLR)
Usa `--arbol` para imprimir en consola cómo ANTLR analizó la estructura jerárquica del código:
```bash
python3 src/main.py examples/ejemplo8_control_y_listas.arc --arbol
```

### Modificar el Límite de Seguridad de Iteraciones
Por defecto, el bucle `mientras` se detiene a las 10,000 iteraciones para prevenir ciclos infinitos. Puedes ajustar este umbral:
```bash
python3 src/main.py examples/ejemplo8_control_y_listas.arc --max-iteraciones 20000
```
