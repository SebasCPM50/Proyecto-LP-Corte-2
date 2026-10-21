# Documento de Alcance — Arcanum
**Curso:** Lenguajes de Programación y Transducción — Semestre 2026-2  
**Corte Actual:** 2 — Semántica y procesamiento de datos  
**Temática:** Alquimia / magia aplicada a un DSL de ciencia de datos  

---

## 1. Motivación y Visión del Proyecto

**Arcanum** es un Lenguaje de Dominio Específico (DSL) diseñado para expresar flujos reproducibles de análisis y preparación de datos. La metáfora central del lenguaje conecta la ciencia de datos con la alquimia: los datos crudos son ingredientes que deben ser limpiados, combinados y destilados para extraer conocimiento valioso.

| Concepto en Arcanum | Concepto en Ciencia de Datos | Objeto Técnico en Python |
|---|---|---|
| **Grimorio** | Archivo de código fuente (`.arc`) | Secuencia de instrucciones AST |
| **Poción** | Conjunto de datos tabular | `pandas.DataFrame` |
| **Ingrediente** | Columna o variable dentro de una tabla | `pandas.Series` / Columna |
| **Transmutación** | Columna calculada a partir de fórmulas | Vectorización de operaciones |
| **Purificación** | Filtro de registros | Indexación booleana (`df[mascara]`) |
| **Sanación** | Tratamiento de valores faltantes/nulos | `dropna()` y `fillna()` |
| **Destilación** | Agrupamiento y agregación estadística | `groupby().agg()` |
| **Preservación** | Exportación de resultados a CSV | `to_csv()` |
| **Artefacto** | Visualización gráfica (Corte 3) | Gráficas en `matplotlib` |

---

## 2. Alcance Alcanzado en el Corte 2

El sistema ahora procesa datos reales de punta a punta, satisfaciendo la totalidad de los entregables y alcances del Segundo Corte:

1. **Lectura y almacenamiento**: Invocación de archivos CSV con resolución automática de rutas.
2. **Selección y proyección**: Recolección de columnas específicas.
3. **Filtrado con condiciones lógicas**: Expresiones booleanas compuestas (`y`, `o`, `no`, comparadores `>`, `<`, `>=`, `<=`, `==`, `!=`).
4. **Columnas calculadas**: Fórmulas aritméticas con precedencia completa (`^`, `*`, `/`, `%`, `+`, `-`).
5. **Tratamiento de nulos**: Sanación mediante descarte de filas con nulos o relleno específico.
6. **Ordenamiento**: Orden ascendente y descendente por columnas numéricas o textuales.
7. **Agrupamiento y agregaciones**: Agrupación multivariable con funciones estadísticas (`suma`, `media`, `mediana`, `minimo`, `maximo`, `desviacion`, `contar`).
8. **Estadísticas descriptivas**: Resumen estadístico imprimible o asignable a variables (`describir`).
9. **Exportación de resultados**: Guardado de tablas resumen a archivos CSV externos (`preservar`).
10. **Diagnóstico semántico**: Reporte detallado de variables o columnas inexistentes y tipos incompatibles con línea y columna.

---

## 3. Entradas, Salidas y Producto Verificable

| Componente | Entrada | Salida |
|---|---|---|
| **Front-End (ANTLR)** | Archivo de texto `.arc` | Árbol de análisis sintáctico (AST) o reporte de errores léxicos/sintácticos |
| **Back-End (Visitor + Pandas)** | Árbol AST + Archivos CSV | Pociones en memoria (`TablaSimbolos`), estadísticas en pantalla y archivos CSV en `salidas/` |

**Producto Verificable**: El DSL procesa conjuntos de datos reales y genera tablas resumen exportadas en formato CSV de manera reproducible y sin errores.
