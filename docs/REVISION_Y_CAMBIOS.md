# Revisión de la versión simplificada

La entrega se centra en aprender el lenguaje y analizar tablas pequeñas.

| Objetivo | Implementación y guía |
|---|---|
| Bucles y condicionales | si/sino, mientras y para; límite configurable de iteraciones y ejemplos con resultados esperados. |
| Estructuras de datos | Tablas como listas de diccionarios, arreglos, matrices, tabla de símbolos y pila de ámbitos locales; explicadas en el manual. |
| Repartir responsabilidades | Control, expresiones, recetas, ámbitos y funciones nativas en src/runtime; lectura y escritura en datos_io; estructuras y gráficas en sus módulos. |
| Flexibilidad | CSV, JSON y Excel como entrada; CSV y JSON como salida; recetas reutilizables, tablas creadas desde listas, selección, filtros, cálculos y agrupaciones. |

## Correcciones conservadas

- Las recetas respetan variables locales, devoluciones y operaciones sobre tablas.
- El análisis comprueba la sintaxis antes de ejecutar instrucciones.
- Potencias, índices, signo negativo y operadores lógicos respetan su precedencia.
- CSV admite comas, comillas y saltos de línea dentro de celdas.
- Los nulos quedan al final al ordenar; contar(columna) cuenta valores no nulos.
- Los ejemplos de factorial, Excel y primos funcionan desde el lenguaje.

## Límites y verificación

El lenguaje interpreta un árbol de análisis: no genera código máquina. No incluye asignación por índice, break, continue ni exportación a Excel. Las gráficas usan Matplotlib y la lectura Excel usa openpyxl. El proyecto incluye los analizadores generados por ANTLR.

Consulta VERIFICACION.txt para los resultados de las pruebas de la entrega y manual_usuario.md o MANUAL_ARCANUM.docx para instrucciones, ejemplos y explicación del código.
