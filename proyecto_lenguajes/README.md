# Arcanum — Lenguaje de Dominio Específico para Ciencia de Datos

![Versión](https://img.shields.io/badge/Corte-Segundo%20Corte%20(Semántica%20y%20Procesamiento)-blueviolet)
![Dependencias](https://img.shields.io/badge/Librerías%20Externas-0%20(Cero%20Pandas%2C%20Cero%20NumPy)-success)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20(Nativo)-blue)
![Tests](https://img.shields.io/badge/Tests-24%20passing%20(100%25)-brightgreen)

**Arcanum** es un Lenguaje de Dominio Específico (DSL) diseñado para expresar flujos reproducibles de carga, preparación, transformación, análisis y exportación de datos bajo una atractiva temática de **alquimia y magia**.

Proyecto desarrollado para la asignatura de **Lenguajes de Programación y Transducción** — Universidad Sergio Arboleda (Semestre 2026-2).  
**Docente:** Joaquín F. Sánchez.

---

## 💎 Característica Distintiva: 100% Artesanal y Cero Librerías Externas

A diferencia de proyectos que delegan todo el trabajo en librerías prefabricadas como Pandas o NumPy:
1. **Estructura de Datos `Pocion` Creada desde Cero (`src/pocion.py`)**:  
   Implementada únicamente con **listas y diccionarios nativos de Python**. Gestiona lectura de CSV, formateo de texto, selección de columnas, filtrado, ordenamiento, columnas calculadas y agregaciones estadísticas manuales (sumas, medias, medianas, desviaciones estándar, conteos).
2. **Sistema de Módulos Propios ("Compendios" y "Recetas")**:  
   Permite crear y utilizar librerías reutilizables escritas en el propio lenguaje Arcanum (`compendios/*.arc`) que se importan con `usar compendio <nombre>;`, sin tocar el mecanismo de `import` de Python.

---

## 🔮 Metáfora del Lenguaje

En Arcanum, la ciencia de datos es un arte alquímico donde los datos crudos son ingredientes que deben ser refinados para descubrir conocimiento oculto:

- **Grimorio**: El programa completo (`.arc`), la secuencia de hechizos de análisis.
- **Hechizo**: Cada instrucción o línea de código.
- **Poción**: Un conjunto de datos tabular (representado por nuestra clase artesanal `Pocion`). **Principio fundamental:** cada hechizo genera una poción nueva e independiente, jamás se altera una poción existente en su lugar.
- **Ingrediente**: Una columna o variable dentro de una poción.
- **Transmutación**: Creación de una columna calculada a partir de fórmulas matemáticas.
- **Purificación**: Filtrado de filas mediante condiciones lógicas y relacionales.
- **Sanación**: Tratamiento de datos faltantes (descarte de nulos o relleno de valores).
- **Destilación**: Agrupamiento multivariable y agregaciones estadísticas.
- **Preservación**: Exportación de tablas resumen a archivos CSV en disco.
- **Compendio**: Archivo de librería reutilizable con recetas probadas (`compendios/`).
- **Receta**: Función propia reutilizable (`receta nombre(args) { devolver expr; }`).
- **Artefacto**: Visualización gráfica (reconocida sintácticamente; para Corte 3).

---

## 🚀 Alcance del Segundo Corte (Semántica y Procesamiento)

| Componente | Capacidad en Arcanum | Implementación Interna Artesanal |
|---|---|---|
| **Carga de Datos** | `invocar desde "csv/ventas.csv";` | Lectura línea a línea y tipado manual (`open`, `split`, `strip`) |
| **Inspección en Consola** | `revelar ventas;` / `describir ventas;` | Renderizado ASCII con columnas alineadas y cálculo de estadísticas |
| **Selección de Columnas** | `recolectar [col1, col2] de pocion;` | Proyección mediante comprensiones de listas nativas |
| **Filtrado Lógico** | `purificar pocion donde unidades > 0 y precio > 0;` | Evaluación booleana fila por fila |
| **Columnas Calculadas** | `transmutar pocion con total = unidades * precio;` | Evaluación de expresiones aritméticas para cada fila |
| **Tratamiento de Nulos** | `sanar pocion descartar_nulos;`<br>`sanar pocion llenar precio con 0;` | Detección de `None`/vacíos y reemplazo en diccionarios |
| **Ordenamiento** | `ordenar pocion por total desc;` | Algoritmo de ordenamiento seguro con `sorted` nativo |
| **Agrupamiento y Métricas** | `destilar pocion por [ciudad] agregar suma(total) como ingreso, contar() como cantidad;` | Hash-map por claves de grupo y fórmulas matemáticas puras |
| **Librerías Propias** | `usar compendio matematicas;`<br>`res = matematicas.calcular_iva(precio, 0.19);` | Carga y ejecución del AST del compendio sin `import` de Python |
| **Exportación CSV** | `preservar resumen en "salidas/resumen.csv";` | Escritura delimitada por comas manual en archivo de texto |
| **Diagnóstico Semántico** | Detección de variables no declaradas, columnas ausentes y tipos incompatibles | Mensajes amigables con línea y columna |

---

## 🏛️ Patrones de Diseño Utilizados

1. **Patrón Visitor (Comportamiento)**:  
   Implementado en `src/visitor.py` (`ArcanumVisitorEjecutor`). Separa la estructura del árbol sintáctico (AST) de la ejecución en Python. Cada método `visit*` se encarga de un hechizo.
2. **Patrón Tabla de Símbolos (Compiladores / Memoria)**:  
   Implementado en `src/tabla_simbolos.py` (`TablaSimbolos`). Administra las variables en memoria, sus tipos (`POCION`, `NUMERO`, `CADENA`, `BOOLEANO`) y valida semánticamente la existencia de variables y columnas.
3. **Patrón Fachada / Motor de Datos (Estructural)**:  
   Implementado en `src/motor.py` (`MotorDatos`). Conecta el Visitor con la estructura artesanal `Pocion`, manteniendo la simplicidad del código.

---

## 📁 Estructura del Proyecto

```
proyecto_lenguajes-main/
├── grammar/
│   └── Arcanum.g4                  # Gramática ANTLR4 completa (Lexer + Parser)
├── generated/                      # Código generado por ANTLR (Lexer, Parser, Visitor)
├── src/
│   ├── main.py                     # Punto de entrada de ejecución del intérprete
│   ├── visitor.py                  # Ejecutor semántico (Patrón Visitor)
│   ├── tabla_simbolos.py           # Gestor de memoria y tipos (Tabla de Símbolos)
│   ├── pocion.py                   # Estructura de datos tabular artesanal (Sin Pandas)
│   ├── motor.py                    # Motor de datos que conecta operaciones y Pocion
│   └── errores.py                  # Manejador de errores léxicos, sintácticos y semánticos
├── compendios/                     # Librerías propias creadas en Arcanum
│   ├── matematicas.arc             #   recetas de IVA, descuentos, potencias
│   └── estadistica.arc             #   recetas de rangos, porcentajes
├── csv/                            # Conjuntos de datos reales (.csv)
│   ├── ventas.csv
│   ├── estudiantes.csv
│   └── calidad_aire.csv
├── datos/                          # Copia sincronizada de datasets para rutas relativas
├── salidas/                        # Archivos CSV exportados por el DSL
│   ├── resumen_ventas_ciudad.csv
│   ├── resumen_estudiantes.csv
│   └── resumen_calidad_aire.csv
├── examples/                       # Programas en Arcanum (.arc)
│   ├── ejemplo1_analisis_ventas.arc
│   ├── ejemplo2_rendimiento_estudiantil.arc
│   ├── ejemplo3_calidad_aire.arc
│   ├── ejemplo4_compendios_recetas.arc
│   ├── valido_asignaciones.arc
│   ├── valido_completo.arc
│   ├── invalido_semantico_variable.arc
│   ├── invalido_semantico_columna.arc
│   └── invalido_semantico_tipo.arc
├── tests/                          # Suite automatizada de pruebas con pytest
│   ├── test_unitarias.py
│   ├── test_semantica.py
│   └── test_integracion.py
├── docs/                           # Documentación técnica completa
│   ├── 01_documento_alcance.md
│   ├── 02_catalogo_instrucciones.md
│   ├── 03_gramatica_bnf_ebnf.md
│   ├── 04_arquitectura_librerias_futuras.md
│   ├── 05_reglas_semanticas.md
│   └── 06_guia_sustentacion_segundo_corte.md # Guía para sustentar ante el docente
├── requirements.txt                # Únicamente antlr4 runtime y pytest
└── README.md
```

---

## 🏃 Cómo Correr el Intérprete

### 1. Ejecutar un programa en Arcanum
```bash
python src/main.py examples/ejemplo1_analisis_ventas.arc
```

### 2. Ejecutar la demostración de librerías propias (Compendios y Recetas)
```bash
python src/main.py examples/ejemplo4_compendios_recetas.arc
```

### 3. Correr las pruebas automáticas con pytest (24 pruebas pasando al 100%)
```bash
python -m pytest -v tests
```

---

## 📖 Documentación Adicional
- [Documento de Alcance](docs/01_documento_alcance.md)
- [Catálogo de Instrucciones](docs/02_catalogo_instrucciones.md)
- [Gramática Formal EBNF](docs/03_gramatica_bnf_ebnf.md)
- [Documento de Reglas Semánticas](docs/05_reglas_semanticas.md)
- [Guía Definitiva para Sustentación](docs/06_guia_sustentacion_segundo_corte.md)
