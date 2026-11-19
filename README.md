# Arcanum: Lenguaje de Dominio Específico (DSL) para Manipulación y Análisis de Tablas

**Arcanum** es un lenguaje de dominio específico (DSL) diseñado para la manipulación tabular, análisis exploratorio de datos (EDA), programación funcional con recetas, transformaciones matriciales y generación de artefactos visuales en PNG.

Su compilador/intérprete está implementado en **Python 3** utilizando **ANTLR4** para el análisis léxico y sintáctico, y ejecuta directamente sobre el Árbol de Análisis Sintáctico mediante una arquitectura modularizada en `src/runtime/`.

---

## Estructura del Repositorio

Todas las carpetas del proyecto se encuentran organizadas directamente en la raíz:

```
Proyecto-LP-Final/
├── src/                        # Núcleo del intérprete y compilador
│   ├── runtime/                # Control de flujo, expresiones, recetas, ámbitos y nativas
│   ├── estructuras/            # Arreglo y Matriz (álgebra lineal)
│   ├── visualizacion/          # Motor de artefactos gráficos PNG (Matplotlib sin GUI)
│   ├── motor.py                # Fachada central de operaciones de datos
│   ├── pocion.py               # Motor tabular artesanal en memoria (Pocion)
│   ├── datos_io.py             # Lectura y guardado de archivos (CSV, JSON, Excel .xlsx)
│   └── main.py                 # Punto de entrada CLI con soporte de flags
├── grammar/                    # Gramática formal del lenguaje (Arcanum.g4)
├── generated/                  # Lexer, Parser y Visitor generados por ANTLR 4.13.2
├── examples/                   # 3 programas .arc esenciales (control, datos y retos)
├── datos/                      # Datasets de entrada (CSV, JSON, Excel .xlsx)
├── csv/                        # Datasets alternativos compatibles
├── compendios/                 # Módulos y librerías reutilizables en Arcanum
├── salidas/                    # Tablas (.csv, .json) y gráficas (.png) exportadas
├── scripts/                    # Scripts de verificación automatizada del compilador
├── tests/                      # Suite de 64 pruebas unitarias y de integración (pytest)
├── docs/                       # Guía oficial y registros de verificación
├── COMO_CORRER.md              # Guía rápida de comandos de ejecución
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

Para auditar que todo el analizador y motor tabular funcionen al 100%:

```bash
# 1. Ejecutar las 64 pruebas automáticas
pytest -q

# 2. Ejecutar el verificador de los ejemplos oficiales
python3 scripts/verificar_ejemplos.py
```

*Resultado esperado*: **64 passed in ~1s** y **3 ejemplos revisados con 0 fallos inesperados**.

---

## Los 3 Ejemplos Oficiales de Arcanum

| Archivo | Enfoque Principal | Salida Obtenida |
|---|---|---|
| **`ejemplo8_control_y_listas.arc`** | Variables, condicionales `si / sino`, ciclo `mientras` con acumulador y listas. | Impresión clara en consola |
| **`ejemplo1_analisis_ventas.arc`** | Pipeline ETL completo en CSV: imputación de nulos, filtros, subtotales y `destilar` por ciudad. | `salidas/resumen_ventas_ciudad.csv` |
| **`ejemplo7_casos_profesor.arc`** | Los retos del profesor: Factorial con ciclo `mientras`, EDA de Excel y filtro de Primos. | `salidas/7_eda_pasajeros_excel.png` |

Para más detalles, consulta **[COMO_CORRER.md](COMO_CORRER.md)**.

---

## Documentación Oficial

En la carpeta `docs/` se encuentra la documentación técnica:
* **[manual_usuario.md](docs/manual_usuario.md)**: Manual del usuario y referencia de sintaxis de Arcanum.
* **[VERIFICACION.txt](docs/VERIFICACION.txt)**: Registro de auditoría y pruebas del sistema.
