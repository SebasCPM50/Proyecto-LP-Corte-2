# Guía Rápida de Ejecución de Arcanum

Esta guía explica de forma directa cómo instalar dependencias, ejecutar los **3 programas oficiales** de Arcanum y correr las pruebas automáticas.

---

## 1. Instalación de Dependencias

Se requiere **Python 3.10 o superior**. El analizador de ANTLR ya está generado en `generated/`, por lo que **no necesitas Java instalado**.

### Opción A: Con Entorno Virtual
#### Linux / macOS:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py examples/ejemplo8_control_y_listas.arc
```

#### Windows (PowerShell):
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py examples/ejemplo8_control_y_listas.arc
```

### Opción B: Instalación Global Directa (Sin Entorno Virtual)
```bash
pip install antlr4-python3-runtime==4.13.2 pytest matplotlib openpyxl
python3 src/main.py examples/ejemplo8_control_y_listas.arc
```

---

## 2. Los 3 Ejemplos Oficiales de Arcanum

La carpeta `examples/` contiene exclusivamente los 3 programas esenciales para aprender, demostrar y sustentar el lenguaje:

### Ejemplo 1: Control de Flujo Básico y Listas (El más sencillo de sintaxis)
**`examples/ejemplo8_control_y_listas.arc`**
* **Qué demuestra**: Variables, condicionales `si / sino`, ciclo `mientras` con acumulador ($1+2+3+4+5=15$) y listas (`Arreglo`).
* **Ejecutar**:
  ```bash
  python3 src/main.py examples/ejemplo8_control_y_listas.arc
  ```

### Ejemplo 2: Análisis de Ventas de Aerolínea en CSV (El más completo de datos)
**`examples/ejemplo1_analisis_ventas.arc`**
* **Qué demuestra**: Carga de boletos de vuelos comerciales (`invocar`), limpieza de valores nulos (`sanar`), filtrado de compras inválidas (`purificar`), cálculo de totales (`transmutar`), agrupación por ciudad destino (`destilar`) y exportación a CSV (`preservar`).
* **Ejecutar**:
  ```bash
  python3 src/main.py examples/ejemplo1_analisis_ventas.arc
  ```
* **Salida producida**: `salidas/resumen_ventas_ciudad.csv`.

### Ejemplo 3: Los Retos del Profesor (Factorial, Excel y Primos)
**`examples/ejemplo7_casos_profesor.arc`**
* **Qué demuestra**:
  1. Función factorial con ciclo `mientras` ($5! = 120$, $10! = 3,628,800$).
  2. Análisis exploratorio de datos de Excel (`datos/Data.xlsx`) con generación de gráfica de barras `salidas/7_eda_pasajeros_excel.png`.
  3. Filtro funcional de números primos del 2 al 30 con `filtrar(rango(2, 31), "es_primo")`.
* **Ejecutar**:
  ```bash
  python3 src/main.py examples/ejemplo7_casos_profesor.arc
  ```

---

## 3. Pruebas y Verificación Automatizada

```bash
# 1. Correr las 64 pruebas unitarias e integración (pytest)
pytest -q

# 2. Correr el verificador de los ejemplos oficiales
python3 scripts/verificar_ejemplos.py
```
*Salida esperada*: **64 passed in ~1s** y **3 ejemplos revisados; 0 fallos inesperados**.
