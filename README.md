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
├── examples/                   # Programas .arc listos para ejecutar
├── datos/                      # Datasets de entrada (CSV, JSON, Excel .xlsx)
├── csv/                        # Datasets alternativos compatibles
├── compendios/                 # Módulos y librerías reutilizables en Arcanum
├── salidas/                    # Tablas (.csv, .json) y gráficas (.png) exportadas
├── scripts/                    # Scripts de verificación automatizada del compilador
├── tests/                      # Suite de 64 pruebas unitarias y de integración (pytest)
├── docs/                       # Guía breve (.docx), auditoría y documentación
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

Para auditar que todo el analizador y motor tabular funcionen al 100%:

```bash
# 1. Ejecutar las 64 pruebas automáticas
pytest -q

# 2. Ejecutar el verificador de los 21 ejemplos
python3 scripts/verificar_ejemplos.py
```

*Resultado esperado*: **64 passed in ~1s** y **21 ejemplos revisados con 0 fallos inesperados**.

---

## Ruta Rápida de Estudio para Sustentación

Para no abrumarse con demasiados ejemplos, la **Guía Breve de Arcanum** sugiere revisar estos 4 programas clave:

1. **`examples/valido_asignaciones.arc`**: Asignación de variables, tipos básicos (enteros, decimales, texto, booleanos) y operaciones con precedencia.
2. **`examples/ejemplo8_control_y_listas.arc`**: Toma de decisiones con `si/sino`, bucle `mientras` con acumulador y recorrido de listas con `para`.
3. **`examples/ejemplo11_tablas_y_recetas.arc`**: Creación de tablas directas en código con `tabla(...)`, filtrado con `purificar`, cálculo con `transmutar` y resumen con `destilar`.
4. **`examples/ejemplo7_casos_profesor.arc`**: Los ejercicios del profesor: Factorial de números grandes, análisis exploratorio de Excel (`Data.xlsx`) con gráfica y filtro de números primos.

Para consultar el catálogo completo de ejemplos de negocio (ventas de aerolíneas, calidad del aire, multiformato JSON, matrices), consulta **[COMO_CORRER.md](COMO_CORRER.md)**.

---

## Documentación y Sustentación

En la carpeta `docs/` se encuentra toda la documentación técnica:
* **[MANUAL_ARCANUM.docx](docs/MANUAL_ARCANUM.docx)**: Guía breve oficial de 4 páginas con todo lo necesario para la sustentación y repaso rápido.
* **[manual_usuario.md](docs/manual_usuario.md)**: Versión en texto plano de la guía breve.
* **[REVISION_Y_CAMBIOS.md](docs/REVISION_Y_CAMBIOS.md)**: Informe de revisión de requisitos y refactorización arquitectónica.
* **[VERIFICACION.txt](docs/VERIFICACION.txt)**: Registro de auditoría y pruebas del sistema.
