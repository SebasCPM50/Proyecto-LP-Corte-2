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
├── examples/                   # 22 programas .arc (15 válidos y 7 de prueba de errores)
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

Para auditar la suite completa de pruebas y verificar los 22 ejemplos del lenguaje:

```bash
# 1. Ejecutar las 81 pruebas automáticas
pytest -q

# 2. Ejecutar el verificador de los 22 ejemplos
python3 scripts/verificar_ejemplos.py
```

*Resultado*: **81 passed in ~3s** y **22 ejemplos revisados con 0 fallos inesperados**.

---

## Resumen de Ejemplos Principales

| Archivo | Dominio / Propósito | Salidas Producidas |
|---|---|---|
| `ejemplo8_control_y_listas.arc` | Introducción a variables, condicionales `si/sino`, bucle `mientras` y listas. | Impresión en consola |
| `ejemplo9_estructuras_funcionales.arc` | Programación funcional (`mapear`, `filtrar`, `reducir`) y matrices. | Impresión en consola |
| `ejemplo10_ml_paso_a_paso.arc` | Los 4 algoritmos de Machine Learning ejecutados de forma limpia e individual. | Predicciones de ML |
| `ejemplo11_tablas_y_recetas.arc` | Creación de tablas directas en código sin archivos y manipulación en recetas. | `salidas/ejemplo11_resumen.csv` |
| `ejemplo1_analisis_ventas.arc` | Pipeline ETL de ventas aéreas (imputación de nulos, filtros, subtotales y `destilar`). | `salidas/resumen_ventas_ciudad.csv` |
| `ejemplo5_caso_estudio_final.arc` | Caso integral: EDA, regresión, KNN, K-Means y 4 gráficos PNG. | 4 imágenes `.png` y CSV/JSON |
| `ejemplo6_analisis_vuelos_json.arc` | Analítica de vuelos leyendo formato nativo **JSON** y gráfica de barras. | `salidas/5_grafica_retraso_aerolineas.png` |
| `ejemplo7_casos_profesor.arc` | Factorial (5 a 100), Sigmoide real calculada, MLP XOR, EDA de Excel y Primos. | `salidas/6_grafica_sigmoide_tendencia.png`, `8_perdida_xor.png`, CSVs |

Para una guía completa paso a paso de cada ejemplo, consulta **[COMO_CORRER.md](COMO_CORRER.md)**.

---

## Documentación y Sustentación

En la carpeta `docs/` se encuentra toda la documentación técnica:
* **[MANUAL_ARCANUM.docx](docs/MANUAL_ARCANUM.docx)**: Manual formal de 24 páginas con teoría, guía de estudio, preguntas frecuentes y guion de 10 minutos para la sustentación.
* **[REVISION_Y_CAMBIOS.md](docs/REVISION_Y_CAMBIOS.md)**: Informe de revisión de requisitos y refactorización arquitectónica.
* **[VERIFICACION.txt](docs/VERIFICACION.txt)**: Registro de auditoría y pruebas del sistema.
* **[docs/historico/](docs/historico/)**: Archivo histórico con versiones previas de guías y catálogos.
