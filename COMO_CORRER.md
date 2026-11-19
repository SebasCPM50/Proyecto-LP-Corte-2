# Guía de Ejecución y Pruebas de Arcanum

Este documento explica de forma detallada cómo instalar dependencias, ejecutar cada uno de los 22 programas de ejemplo y verificar las pruebas unitarias del compilador/intérprete **Arcanum**.

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
*Resultado esperado*: `81 passed in ~3s`.

### B. Correr el verificador de los 22 ejemplos
```bash
# Con entorno virtual:
.venv/bin/python scripts/verificar_ejemplos.py

# O globalmente:
python3 scripts/verificar_ejemplos.py
```
*Resultado esperado*: `22 ejemplos revisados; 0 fallos inesperados`.

---

## 3. Catálogo de Ejecución de Ejemplos Principales

Para ejecutar cualquier ejemplo, usa la sintaxis:
```bash
python3 src/main.py examples/<nombre_del_ejemplo>.arc
```

### A. Ruta Pedagógica Paso a Paso (Aprender desde cero)

#### Ejemplo 8: Control de Flujo, Variables y Listas
Muestra variables, condicionales `si/sino`, bucle `mientras`, acumuladores y listas.
```bash
python3 src/main.py examples/ejemplo8_control_y_listas.arc
```

#### Ejemplo 9: Programación Funcional y Matrices
Muestra operaciones funcionales (`mapear`, `filtrar`, `reducir`) y álgebra lineal con matrices.
```bash
python3 src/main.py examples/ejemplo9_estructuras_funcionales.arc
```

#### Ejemplo 10: Machine Learning Paso a Paso
Muestra de forma aislada y limpia los 4 modelos de ML: Regresión Lineal, Clasificador KNN, Agrupamiento K-Means y Perceptrón Multicapa (XOR).
```bash
python3 src/main.py examples/ejemplo10_ml_paso_a_paso.arc
```

#### Ejemplo 11: Tablas en Memoria y Recetas
Crea una Poción desde listas de código sin archivo físico, calcula totales y exporta a `salidas/ejemplo11_resumen.csv`.
```bash
python3 src/main.py examples/ejemplo11_tablas_y_recetas.arc
```

---

### B. Casos de Estudio y Negocio

#### Ejemplo 1: Análisis de Ventas de Aerolínea (CSV)
Carga boletos de vuelos internacionales, sana nulos en descuentos, purifica filas inválidas, calcula subtotales/totales, agrupa por ciudad y exporta a `salidas/resumen_ventas_ciudad.csv`.
```bash
python3 src/main.py examples/ejemplo1_analisis_ventas.arc
```

#### Ejemplo 2: Rendimiento Estudiantil (CSV)
Filtra por asistencia mínima (>= 75%), promedia parciales y agrupa por carrera. Exporta a `salidas/resumen_estudiantes.csv`.
```bash
python3 src/main.py examples/ejemplo2_rendimiento_estudiantil.arc
```

#### Ejemplo 3: Monitoreo de Calidad del Aire (CSV)
Imputa partículas PM10 faltantes con valor 50, filtra lecturas positivas y agrupa por estación de monitoreo. Exporta a `salidas/resumen_calidad_aire.csv`.
```bash
python3 src/main.py examples/ejemplo3_calidad_aire.arc
```

#### Ejemplo 4: Compendios y Librerías Externas (.arc)
Demuestra el uso de la cláusula `usar compendio matematicas;` y `usar compendio estadistica;`.
```bash
python3 src/main.py examples/ejemplo4_compendios_recetas.arc
```

#### Ejemplo 5: Caso de Estudio Integral (ML, Matrices y 4 Gráficas PNG)
Pipeline completo que entrena Regresión, KNN, K-Means, y genera 4 gráficos visuales en `salidas/`.
```bash
python3 src/main.py examples/ejemplo5_caso_estudio_final.arc
```

#### Ejemplo 6: Analítica de Vuelos Comerciales y Retrasos (JSON)
Demuestra la lectura nativa de archivos **JSON** (`datos/vuelos.json`), agrupa retrasos por aerolínea, genera la gráfica de barras `salidas/5_grafica_retraso_aerolineas.png` y exporta el resultado a JSON.
```bash
python3 src/main.py examples/ejemplo6_analisis_vuelos_json.arc
```

#### Ejemplo 7: Los 5 Problemas del Profesor
Ejecuta los 5 ejercicios del tablero:
1. Función factorial ($5!$, $10!$ y $100!$).
2. Función Sigmoide matemática real calculando 13 puntos y graficando `salidas/6_grafica_sigmoide_tendencia.png`.
3. Perceptrón Multicapa resolviendo el problema no lineal XOR con curva de pérdida `salidas/8_perdida_xor.png`.
4. Análisis exploratorio de datos de Excel (`datos/Data.xlsx`) con gráfica `salidas/7_eda_pasajeros_excel.png`.
5. Filtro funcional de números primos del 2 al 30.
```bash
python3 src/main.py examples/ejemplo7_casos_profesor.arc
```

---

## 4. Ejemplos de Validación de Errores (7 Casos Inválidos)

El compilador incluye validaciones para atrapar errores y detener la ejecución de forma segura con código de salida 1:

| Archivo | Tipo de Error Demostrado |
|---|---|
| `examples/invalido_lexico.arc` | Cadena de texto sin cerrar comillas |
| `examples/invalido_lexico_caracter.arc` | Carácter ilegal no reconocido (`~`) |
| `examples/invalido_sintactico.arc` | Expresión incompleta y sintaxis mal formada |
| `examples/invalido_sintactico_recolectar.arc` | Omisión de palabra reservada obligatoria (`de`) |
| `examples/invalido_semantico_variable.arc` | Uso de variable no declarada |
| `examples/invalido_semantico_columna.arc` | Consulta de columna inexistente en la tabla |
| `examples/invalido_semantico_tipo.arc` | Operación incompatible de tipos (seleccionar columnas de un número) |

Para probar cualquiera:
```bash
python3 src/main.py examples/invalido_semantico_columna.arc
```

---

## 5. Parámetros Avanzados de la Terminal

### Inspeccionar el Árbol de Análisis Sintáctico (CST/AST de ANTLR)
Usa `--arbol` para imprimir en consola cómo ANTLR analizó la estructura jerárquica del código:
```bash
python3 src/main.py examples/valido_asignaciones.arc --arbol
```

### Modificar el Límite de Seguridad de Iteraciones
Por defecto, el bucle `mientras` se detiene a las 10,000 iteraciones para prevenir ciclos infinitos. Puedes ajustar este umbral:
```bash
python3 src/main.py examples/ejemplo8_control_y_listas.arc --max-iteraciones 20000
```
