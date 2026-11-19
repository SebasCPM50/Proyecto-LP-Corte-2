# Arcanum: Lenguaje de Dominio Específico (DSL) para Ciencia de Datos y Machine Learning

**Arcanum** es un lenguaje de dominio específico (DSL) diseñado para la manipulación tabular, análisis exploratorio de datos (EDA), programación funcional, transformaciones matriciales y experimentación con algoritmos de Machine Learning desde cero. 

Su compilador/intérprete está implementado en **Python 3** utilizando **ANTLR4** para el análisis léxico y sintáctico, y ejecuta directamente sobre el Árbol de Análisis Sintáctico mediante el patrón *Visitor* modularizado.

---

## Estructura del Repositorio

El proyecto está organizado de forma limpia en la raíz del repositorio:

```
Proyecto-LP-Final/
├── src/                        # Núcleo del intérprete y compilador
│   ├── runtime/                # Control de flujo, expresiones, recetas, ámbitos y nativas
│   ├── estructuras/            # Arreglo y Matriz (álgebra lineal)
│   ├── ml/                     # Regresión, KNN, K-Means, Perceptrón Multicapa y validación
│   ├── visualizacion/          # Motor de artefactos gráficos PNG (Matplotlib sin GUI)
│   ├── motor.py                # Fachada central de operaciones de datos
│   ├── pocion.py               # Motor tabular nativo en memoria (Pocion)
│   ├── datos_io.py             # Lectura y guardado de archivos (CSV, JSON, Excel .xlsx)
│   └── main.py                 # Punto de entrada CLI con soporte de flags
├── grammar/                    # Gramática formal del lenguaje (Arcanum.g4)
├── generated/                  # Lexer, Parser y Visitor generados por ANTLR 4.13.2
├── examples/                   # 9 programas .arc oficiales listos para ejecutar
├── datos/                      # Datasets de entrada (CSV, JSON, Excel .xlsx)
├── csv/                        # Datasets alternativos compatibles
├── compendios/                 # Módulos y librerías reutilizables en Arcanum
├── salidas/                    # Tablas (.csv, .json) y gráficas (.png) exportadas
├── scripts/                    # Scripts de verificación automatizada del compilador
├── tests/                      # Suite de 81 pruebas unitarias y de integración (pytest)
├── docs/                       # Manual completo (.docx), cambios y documentación
├── COMO_CORRER.md              # Guía exhaustiva de ejecución y sustentación
├── requirements.txt            # Dependencias mínimas
└── README.md                   # Este archivo
```

---

## Instalación y Primeros Pasos

El repositorio ya contiene los archivos generados por ANTLR en `generated/`, por lo que **no necesitas Java instalado**.

### En Linux / macOS
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py examples/ejemplo8_control_y_listas.arc
```

### En Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py examples/ejemplo8_control_y_listas.arc
```

### Sin Entorno Virtual (Instalación Global)
```bash
pip install antlr4-python3-runtime==4.13.2 pytest matplotlib openpyxl
python3 src/main.py examples/ejemplo8_control_y_listas.arc
```

---

## Verificación del Compilador

Para auditar la suite completa de pruebas y verificar los 9 ejemplos del lenguaje:

```bash
# 1. Ejecutar las 81 pruebas automáticas
pytest -q

# 2. Ejecutar el verificador de los 9 ejemplos oficiales
python3 scripts/verificar_ejemplos.py
```

*Resultado*: **81 passed in ~2s** y **9 ejemplos revisados con 0 fallos inesperados**.

---

## Catálogo de los 9 Ejemplos Oficiales

| Número | Archivo | Dominio / Propósito | Salidas Producidas |
|:---:|---|---|---|
| **1** | `ejemplo1_analisis_ventas.arc` | **Pipeline ETL en CSV**: Limpieza de nulos, filtros, subtotales y agrupación por destino de vuelos. | `salidas/resumen_ventas_ciudad.csv` |
| **2** | `ejemplo2_rendimiento_estudiantil.arc` | **Filtros Académicos**: Asistencia mínima $\ge 75\%$, promedios y carreras universitarias. | `salidas/resumen_estudiantes.csv` |
| **3** | `ejemplo3_calidad_aire.arc` | **Imputación Ambiental**: Relleno de partículas PM10, filtros y agrupación por estación. | `salidas/resumen_calidad_aire.csv` |
| **4** | `ejemplo4_compendios_recetas.arc` | **Compendios y Librerías**: Modularización con `usar compendio matematicas;` y `estadistica;`. | `salidas/ventas_con_librerias_propias.csv` |
| **5** | `ejemplo5_caso_estudio_final.arc` | **Machine Learning Integral**: Regresión Lineal, KNN, K-Means, matrices y 4 gráficos PNG. | 4 imágenes `.png` y CSV/JSON |
| **6** | `ejemplo6_analisis_vuelos_json.arc` | **Analítica Multiformato JSON**: Lectura nativa de `vuelos.json` y gráfica de barras PNG. | `salidas/5_grafica_retraso_aerolineas.png` y JSON |
| **7** | `ejemplo7_casos_profesor.arc` | **Los 5 Ejercicios del Profesor**: Factorial (5 a 100), Sigmoide real, MLP XOR, Excel y Primos. | Gráficas `6` y `8`, CSV de pérdida y sigmoide |
| **8** | `ejemplo8_control_y_listas.arc` | **Fundamentos Básicos**: Variables, condicionales `si/sino`, bucle `mientras` y listas. | Impresión en consola |
| **9** | `ejemplo9_estructuras_funcionales.arc` | **Programación Funcional y Matrices**: `mapear`, `filtrar`, `reducir` y álgebra lineal de matrices. | Impresión en consola |

Para una guía completa paso a paso de cada ejemplo, consulta **[COMO_CORRER.md](COMO_CORRER.md)**.

---

## Documentación y Sustentación

En la carpeta `docs/` se encuentra toda la documentación técnica:
* **[MANUAL_ARCANUM.docx](docs/MANUAL_ARCANUM.docx)**: Manual formal con teoría, guía de estudio, preguntas frecuentes y guion de 10 minutos para la sustentación.
* **[REVISION_Y_CAMBIOS.md](docs/REVISION_Y_CAMBIOS.md)**: Informe de revisión de requisitos y refactorización arquitectónica.
* **[VERIFICACION.txt](docs/VERIFICACION.txt)**: Registro de auditoría y pruebas del sistema.
* **[docs/historico/](docs/historico/)**: Archivo histórico con versiones y ejemplos anteriores.
