# GUÍA DEFINITIVA: CÓMO CORRER CADA PARTE DEL PROYECTO ARCANUM
**Asignatura:** Lenguajes de Programación y Transducción  
**Docente:** Joaquín F. Sánchez | **Universidad Sergio Arboleda**  
**Entrega Final (Corte 3)**

Esta guía contiene todos los comandos exactos y explicaciones paso a paso para ejecutar cada componente del proyecto, tanto en **Windows** como en **Linux (Ubuntu)**.

---

## 1. PREPARACIÓN INICIAL DEL ENTORNO

Antes de ejecutar cualquier código, asegúrate de tener instaladas las dependencias mínimas del sistema:

### En Windows (PowerShell o CMD):
```powershell
# 1. Ubicarse en la raíz del proyecto
cd C:\ruta\al\proyecto

# 2. (Opcional recomendado) Crear y activar un entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar las dependencias del proyecto
pip install -r requirements.txt
```

### En Linux / Ubuntu:
```bash
# 1. Actualizar paquetes del sistema
sudo apt update && sudo apt install -y python3 python3-pip python3-venv default-jre

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

> **Nota sobre librerías:** Arcanum **NO utiliza Pandas ni NumPy** (fueron creados 100% de forma artesanal en `src/pocion.py` y `src/estructuras/matriz.py`). El archivo `requirements.txt` solo instala `antlr4-python3-runtime` (para el analizador léxico/sintáctico), `pytest` (para las pruebas automáticas), `matplotlib` (para exportar los gráficos a imágenes PNG) y `openpyxl` (opcional para lectura directa de archivos Excel `.xlsx`).

---

## 2. CÓMO CORRER LOS 7 PROGRAMAS DE EJEMPLO (.arc)

Todos los programas de Arcanum tienen extensión `.arc` (llamados "Grimorios") y se ejecutan pasando su ruta a `src/main.py`:

```bash
python src/main.py <ruta_al_archivo.arc>
```

---

### Ejemplo 1: Flujo Analítico y Ventas de Boletos Aéreos
* **Archivo:** `examples/ejemplo1_analisis_ventas.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo1_analisis_ventas.arc
  ```
* **Qué hace:**
  1. Carga el dataset de pasajes aéreos desde `csv/ventas.csv`.
  2. Muestra los datos crudos en la terminal con `revelar`.
  3. Imputa los descuentos nulos asignándoles `0.0` con `sanar`.
  4. Selecciona las columnas necesarias con `recolectar`.
  5. Filtra ventas válidas (`unidades > 0 y precio > 0`) con `purificar`.
  6. Calcula el subtotal y total con descuento con `transmutar`.
  7. Ordena de mayor a menor por facturación con `ordenar`.
  8. Destila por destino de vuelo calculando suma de ingresos, promedio de ticket y total de transacciones con `destilar`.
  9. Exporta el reporte tabular a `salidas/resumen_ventas_ciudad.csv`.
* **Salida esperada:** Tablas formateadas en consola y archivo CSV generado en `salidas/`.

---

### Ejemplo 2: Rendimiento Académico Estudiantil
* **Archivo:** `examples/ejemplo2_rendimiento_estudiantil.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo2_rendimiento_estudiantil.arc
  ```
* **Qué hace:**
  1. Carga `datos/estudiantes.csv` con registros de alumnos universitarios.
  2. Imputa notas vacías asignándoles `0.0`.
  3. Agrupa por carrera universitaria y calcula el promedio general de notas.
  4. Exporta el consolidado a `salidas/resumen_estudiantes.csv`.

---

### Ejemplo 3: Monitoreo Ambiental y Calidad del Aire
* **Archivo:** `examples/ejemplo3_calidad_aire.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo3_calidad_aire.arc
  ```
* **Qué hace:**
  1. Carga mediciones de estaciones meteorológicas desde `datos/calidad_aire.csv`.
  2. Descarta registros con celdas nulas con `sanar`.
  3. Filtra estaciones con temperatura $> 18^\circ\text{C}$ con `purificar`.
  4. Calcula la media aritmética y desviación estándar de material particulado PM2.5 por estación con `destilar`.
  5. Exporta el resultado a `salidas/resumen_calidad_aire.csv`.

---

### Ejemplo 4: Sistema de Compendios y Recetas Propias (Librerías)
* **Archivo:** `examples/ejemplo4_compendios_recetas.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo4_compendios_recetas.arc
  ```
* **Qué hace:**
  1. Demuestra la modularidad del lenguaje importando una librería propia escrita en Arcanum: `usar compendio matematicas;`.
  2. Invoca funciones locales y de compendios (`matematicas.calcular_iva`, `matematicas.potencia`).
  3. Exporta los resultados calculados a `salidas/ventas_con_librerias_propias.csv`.

---

### Ejemplo 5: Caso de Estudio Final Integrado (CORTE 3)
* **Archivo:** `examples/ejemplo5_caso_estudio_final.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo5_caso_estudio_final.arc
  ```
* **Qué hace (El flujo completo de Ciencia de Datos):**
  1. **Carga Multiformato:** Carga simultánea de `datos/vuelos.json` y `csv/ventas.csv`.
  2. **Control de Flujo:** Evalúa metas con condicionales `si / sino` y ejecuta bucles `mientras`.
  3. **Álgebra Lineal:** Crea matrices 2D artesanales con `matriz([[1, 2], [3, 4]])` y calcula la `transpuesta`.
  4. **Machine Learning Artesanal:**
     * **Predicción:** Entrena una Regresión Lineal por mínimos cuadrados ($R^2=1.0$) y predice ingresos futuros.
     * **Clasificación:** Entrena un modelo KNN ($K=3$) y clasifica nuevos pasajeros como Frecuente o Corporativo.
     * **Agrupamiento:** Aplica K-Means clustering generando 3 segmentos en la tabla.
  5. **Visualización a PNG:** Forja 4 gráficas de alta resolución (300 DPI):
     * `salidas/1_grafica_barras_ciudades.png`
     * `salidas/2_grafica_lineas_ventas.png`
     * `salidas/3_grafica_dispersion.png`
     * `salidas/4_grafica_histograma_precios.png`
  6. **Exportación Doble:** Guarda los resultados en `salidas/resumen_caso_estudio_final.csv` y `salidas/resumen_caso_estudio_final.json`.

---

### Ejemplo 6: Analítica de Vuelos con Carga Nativa en JSON
* **Archivo:** `examples/ejemplo6_analisis_vuelos_json.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo6_analisis_vuelos_json.arc
  ```
* **Qué hace:**
  1. Lee directamente el archivo `datos/vuelos.json` a memoria.
  2. Purifica los vuelos con retraso (`retraso_min > 0`).
  3. Destila por aerolínea calculando el promedio de retraso y los vuelos afectados.
  4. Genera la gráfica de barras `salidas/5_grafica_retraso_aerolineas.png`.
  5. Exporta el reporte final en formato JSON estructurado a `salidas/resumen_retrasos_aerolineas.json`.

---

### Ejemplo 7: Los 5 Retos de Sustentación en Tablero
* **Archivo:** `examples/ejemplo7_casos_profesor.arc`
* **Comando:**
  ```bash
  python src/main.py examples/ejemplo7_casos_profesor.arc
  ```
* **Qué hace (Demostración de los 5 ejercicios típicos solicitados por el docente):**
  1. **Factorial (# 5 al 100):** Calcula $5! = 120$ y $10! = 3628800$ con enteros de precisión arbitraria mediante una receta iterativa con bucle `mientras`.
  2. **Función Sigmoide $S(x)$:** Calcula $S(0) = 0.5$ y forja la gráfica PNG `salidas/6_grafica_sigmoide_tendencia.png`.
  3. **Perceptrón Multicapa (MLP) para XOR:** Entrena una red neuronal artificial de 2 capas con Backpropagation artesanal para resolver el problema no lineal de XOR, prediciendo exactamente $[0,0]\to 0$, $[0,1]\to 1$, $[1,0]\to 1$, $[1,1]\to 0$.
  4. **Data.xlsx y EDA:** Carga directamente la hoja de cálculo Excel `datos/Data.xlsx`, ejecuta `describir` para obtener conteo, media, desviación, min y max, y forja `salidas/7_eda_pasajeros_excel.png`.
  5. **Filtro de Números Primos:** Evalúa números con la receta pura `es_primo(n)` basada en el operador módulo `%`.

---

## 3. CÓMO VISUALIZAR EL ÁRBOL SINTÁCTICO (AST)

Para ver el árbol de derivación sintáctica que construye ANTLR4 paso a paso en formato visual jerárquico, añade el flag `--arbol` al final de cualquier comando:

```bash
# Ver el árbol del Ejemplo 1
python src/main.py examples/ejemplo1_analisis_ventas.arc --arbol

# Ver el árbol de asignaciones básicas
python src/main.py examples/valido_asignaciones.arc --arbol
```

---

## 4. CÓMO CORRER LA SUITE COMPLETA DE PRUEBAS (46 PRUEBAS)

El proyecto cuenta con **46 pruebas automatizadas** que verifican el 100% de las capas del compilador y motor:

### Correr todas las pruebas juntas:
```bash
python -m pytest tests/ -v
```

### Correr pruebas por módulo específico:
```bash
# 1. Pruebas de la Entrega Final (Control de flujo, NumPy, ML, Gráficos, JSON, Excel)
python -m pytest tests/test_corte3.py -v

# 2. Pruebas Unitarias del DataFrame artesanal (Pocion) y Tabla de Símbolos
python -m pytest tests/test_unitarias.py -v

# 3. Pruebas Semánticas (Validación de errores lógicos controlados)
python -m pytest tests/test_semantica.py -v

# 4. Pruebas de Integración (Ejecución completa de grimorios y validación de salidas)
python -m pytest tests/test_integracion.py -v
```

---

## 5. CÓMO PROBAR LOS ERRORES SEMÁNTICOS CONTROLADOS

Para demostrarle al profesor cómo el analizador semántico captura y reporta anomalías lógicas con número exacto de línea y columna, ejecuta los siguientes programas con errores intencionales:

```bash
# 1. Error de Variable no declarada
python src/main.py examples/invalido_semantico_variable.arc
# Salida: [Error Semántico] Línea 3, Columna 8: La variable o ingrediente 'tasa_desconocida' no ha sido declarada

# 2. Error de Columna que no existe en la tabla
python src/main.py examples/invalido_semantico_columna.arc
# Salida: [Error Semántico] Línea 4, Columna 22: La poción 'ventas' no contiene el ingrediente 'columna_inventada'

# 3. Error de Tipo incompatible (tratar un número como tabla)
python src/main.py examples/invalido_semantico_tipo.arc
# Salida: [Error Semántico] Línea 4, Columna 23: La variable 'tasa_iva' es de tipo NUMERO, no es una POCIÓN
```

---

## 6. DÓNDE SE ENCUENTRAN LAS SALIDAS GENERADAS

Cada vez que ejecutas los grimorios, los archivos resultantes se guardan de forma automática y ordenada en la carpeta `salidas/`:

### Gráficas PNG generadas a 300 DPI:
* `salidas/1_grafica_barras_ciudades.png`: Ingresos totales por destino de vuelo (Barras).
* `salidas/2_grafica_lineas_ventas.png`: Evolución temporal de facturación (Líneas).
* `salidas/3_grafica_dispersion.png`: Relación pasajeros vs precio del boleto (Dispersión).
* `salidas/4_grafica_histograma_precios.png`: Distribución de tarifas de pasajes (Histograma).
* `salidas/5_grafica_retraso_aerolineas.png`: Retraso promedio por aerolínea en minutos (Barras).
* `salidas/6_grafica_sigmoide_tendencia.png`: Curva continua de función sigmoide (Líneas).
* `salidas/7_eda_pasajeros_excel.png`: Análisis exploratorio de pasajeros desde Excel (Barras).

### Reportes tabulares exportados:
* `salidas/resumen_caso_estudio_final.csv`: Consolidado exportado en formato CSV.
* `salidas/resumen_caso_estudio_final.json`: Consolidado exportado en formato JSON estructurado.
* `salidas/resumen_retrasos_aerolineas.json`: Reporte de puntualidad en JSON.
* `salidas/resumen_ventas_ciudad.csv`: Resumen de ventas por destino en CSV.

---

## 7. CÓMO REGENERAR LA GRAMÁTICA ANTLR4 (SI FUERA NECESARIO)

Si el profesor te pide recompilar la gramática formal `grammar/Arcanum.g4` para regenerar el Parser y Lexer en Python:

```bash
# Comando estándar con el JAR de ANTLR4:
java -jar /ruta/a/antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener -o generated grammar/Arcanum.g4
```
*(Los archivos autogenerados se encuentran organizados dentro de la carpeta `generated/`).*
