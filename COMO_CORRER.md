# Guía Completa de Ejecución y Estudio de Arcanum

Esta guía explica paso a paso cómo instalar dependencias, ejecutar los ejemplos clave del lenguaje y correr la batería de pruebas automatizadas del proyecto **Arcanum**.

---

## 1. Instalación y Primeros Pasos

Necesitas **Python 3.10 o posterior**. El repositorio ya incluye el lexer y parser generados por ANTLR en `generated/`, por lo que **no requieres tener Java instalado**.

### Opción A: Con Entorno Virtual (Recomendada)

#### En Linux o macOS:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py examples/ejemplo8_control_y_listas.arc
```

#### En Windows (PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py examples/ejemplo8_control_y_listas.arc
```

### Opción B: Sin Entorno Virtual (Instalación Global)

#### En Ubuntu / Debian:
```bash
pip3 install antlr4-python3-runtime==4.13.2 pytest matplotlib openpyxl --break-system-packages
python3 src/main.py examples/ejemplo8_control_y_listas.arc
```

#### En Windows:
```powershell
pip install antlr4-python3-runtime==4.13.2 pytest matplotlib openpyxl
python src/main.py examples/ejemplo8_control_y_listas.arc
```

> **Regla de Oro**: Ejecuta siempre desde la **carpeta raíz del proyecto** (donde están `src/`, `examples/` y `requirements.txt`). Nunca ejecutes comandos desde dentro de `src/`.

---

## 2. Verificación Automatizada del Compilador

Para auditar que todo el analizador sintáctico, el motor tabular y los módulos funcionen a la perfección:

### A. Correr las 64 Pruebas Unitarias e Integración (pytest)
```bash
pytest -q
```
*Salida esperada*: `64 passed in ~1s`.

### B. Correr el Verificador de los 21 Ejemplos
```bash
python3 scripts/verificar_ejemplos.py
```
*Salida esperada*: `21 ejemplos revisados; 0 fallos inesperados`.

---

## 3. Ruta Sugerida de Estudio para la Sustentación (Los 4 Claves)

Para no saturarse con demasiados códigos, la **Guía Breve de Arcanum** recomienda enfocarse en estos 4 programas en orden:

### 1. Variables y Operaciones Básicas
**`examples/valido_asignaciones.arc`**
* **Qué hace**: Asignación de enteros, decimales, textos, booleanos y cálculos aritméticos con precedencia.
* **Comando**:
  ```bash
  python3 src/main.py examples/valido_asignaciones.arc
  ```
* **Qué observar**: El resultado final `total_con_descuento` da `212.5`.

### 2. Decisiones, Bucles y Listas
**`examples/ejemplo8_control_y_listas.arc`**
* **Qué hace**: Demuestra condicionales `si/sino`, bucle `mientras` con acumulador, y recorrido de listas con `para`.
* **Comando**:
  ```bash
  python3 src/main.py examples/ejemplo8_control_y_listas.arc
  ```
* **Qué observar**: Imprime "Hola, Arcanum", la evaluación de nota "Aprobado", y el acumulado `15` ($1+2+3+4+5$).

### 3. Manejo de Tablas en Código y Recetas
**`examples/ejemplo11_tablas_y_recetas.arc`**
* **Qué hace**: Construye una tabla en memoria con `tabla(...)` sin necesidad de archivos externos, filtra con `purificar`, calcula con `transmutar`, agrupa con `destilar` y exporta a CSV.
* **Comando**:
  ```bash
  python3 src/main.py examples/ejemplo11_tablas_y_recetas.arc
  ```
* **Qué observar**: Muestra la tabla filtrada y genera `salidas/ejemplo11_resumen.csv`.

### 4. Los Ejercicios del Profesor (Factorial, Excel y Primos)
**`examples/ejemplo7_casos_profesor.arc`**
* **Qué hace**: 
  1. Receta factorial con bucle `mientras` ($5! = 120$, $10! = 3,628,800$).
  2. Lectura y análisis exploratorio (EDA) de hoja de cálculo Excel (`datos/Data.xlsx`) exportando gráfica a `salidas/7_eda_pasajeros_excel.png`.
  3. Filtro funcional de números primos del 2 al 30 usando `filtrar(rango(2, 31), "es_primo")`.
* **Comando**:
  ```bash
  python3 src/main.py examples/ejemplo7_casos_profesor.arc
  ```

---

## 4. Otros Casos de Negocio y Datos

| Ejemplo | Descripción | Comando |
|---|---|---|
| **Ejemplo 1** | ETL de ventas de boletos aéreos CSV (limpieza de nulos, subtotales y agrupación por destino). | `python3 src/main.py examples/ejemplo1_analisis_ventas.arc` |
| **Ejemplo 2** | Rendimiento académico estudiantil (filtro de asistencia $\ge 75\%$ y promedios por carrera). | `python3 src/main.py examples/ejemplo2_rendimiento_estudiantil.arc` |
| **Ejemplo 3** | Monitoreo ambiental de calidad del aire (imputación con `sanar` y métricas PM10 por estación). | `python3 src/main.py examples/ejemplo3_calidad_aire.arc` |
| **Ejemplo 4** | Compendios y librerías reutilizables (`usar compendio matematicas;` y `estadistica;`). | `python3 src/main.py examples/ejemplo4_compendios_recetas.arc` |
| **Ejemplo 5** | Caso de estudio integral multiformato (CSV + JSON, matrices y 4 gráficas PNG). | `python3 src/main.py examples/ejemplo5_caso_estudio_final.arc` |
| **Ejemplo 6** | Analítica de vuelos en formato nativo **JSON** (`datos/vuelos.json`) con gráfica de barras. | `python3 src/main.py examples/ejemplo6_analisis_vuelos_json.arc` |
| **Ejemplo 9** | Programación funcional (`mapear`, `filtrar`, `reducir`) y matrices numéricas. | `python3 src/main.py examples/ejemplo9_estructuras_funcionales.arc` |

---

## 5. Parámetros Avanzados

### Inspeccionar el Árbol Sintáctico (AST / CST de ANTLR)
```bash
python3 src/main.py examples/valido_asignaciones.arc --arbol
```

### Configurar Límite de Iteraciones
```bash
python3 src/main.py examples/ejemplo8_control_y_listas.arc --max-iteraciones 20000
```
