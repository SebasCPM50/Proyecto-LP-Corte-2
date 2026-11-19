# Revisión de los requisitos de Arcanum
Fecha de entrega: 18 de noviembre de 2026.

## Qué había en la versión recibida
| Requisito | Estado comprobado antes | Resultado de esta entrega |
|---|---|---|
| Bucles y condicionales | Ya existían si/sino, mientras y para en gramática y visitor | Conservados; booleanos directos, cortocircuito, negativos, precedencia corregida y límite configurable |
| Estudiar estructuras de datos | Ya existían Arreglo, Matriz, Pocion y tabla de símbolos; la explicación tenía nombres y afirmaciones imprecisas | Manual de representación, operaciones y complejidad; mapear/filtrar/reducir accesibles desde .arc; validación rectangular |
| Introducir Machine Learning | Ya estaban regresión lineal, KNN, K-Means y MLP conectados al lenguaje | Se conservan y validan tamaños, números y parámetros; predicción por lotes, probabilidad e historial disponibles |
| Repartir responsabilidades | Ya existían motor, estructuras, ml y visualización, pero visitor y pocion seguían concentrando tareas | Visitor reducido de 769 a 320 líneas y Pocion de 635 a 299; nuevos módulos runtime, datos_io, aleatorio y analizador |
| Flexibilizar el lenguaje | Había recetas, compendios y entrada CSV/JSON/Excel | Funciones nativas registrables, rango con paso, tablas sin archivo, acceso a columnas, operaciones de matrices, retorno anticipado y ámbitos coherentes |

Los conteos de líneas anteriores se verifican contra la copia recibida; no son por sí solos una medida de calidad.

## Correcciones concretas
- El ejemplo 7 dibujaba precio de vuelos contra retraso bajo el título Sigmoide. Ahora calcula 13 puntos reales de -6 a 6, exporta los valores y dibuja la curva.
- El ejemplo 7 ahora filtra una colección de primos y grafica la pérdida del MLP; también demuestra factorial de 100.
- Se agregaron datos/clientes.csv y datos/inventario.csv, ausentes aunque los ejemplos válidos los referenciaban.
- CSV usa el módulo estándar csv para conservar comas, comillas y saltos de línea dentro de una celda.
- Ordenar descendente deja los nulos al final; contar(columna) cuenta valores no nulos y contar() cuenta filas.
- Las recetas pueden mostrar y transformar tablas locales sin buscar equivocadamente solo variables globales.
- Los compendios se analizan antes de cargarlos y solo aceptan definiciones de recetas.
- KNN rechaza dimensiones distintas; K-Means rechaza k inválido y calcula correctamente el centroide incluso con un solo grupo; MLP rechaza datos vacíos, etiquetas no binarias y predicción sin entrenar.
- Las funciones nativas informan errores semánticos y validan la cantidad de argumentos.
- Se eliminó el lector Excel alternativo incompleto: .xlsx usa openpyxl; .xls se rechaza explícitamente.
- El intérprete ahora admite mostrar expresiones, signo negativo, índices con precedencia alta, potencias asociadas a la derecha y devolución dentro de un condicional o bucle.

## Validación
La copia original pasó 46 pruebas. La versión mejorada pasó 81 pruebas automatizadas y el verificador de los 22 ejemplos: 15 válidos y 7 inválidos intencionales, sin fallos inesperados. Se validó en macOS con Python 3.15; no se ejecutó una sesión Windows. Los comandos Windows usan el entorno virtual estándar de Python.

Se conserva la API principal de Pocion, MotorDatos, ejecutar y ArcanumVisitorEjecutor. Se regeneraron lexer, parser, listener y visitor con ANTLR 4.13.2. Los datos y salidas son material educativo; no hay evidencia adjunta de que provengan de operaciones reales.

## Límites que conviene explicar
- ML es educativo: no hay separación automática entrenamiento/prueba, ajuste de hiperparámetros, escalado automático ni guardado/carga de modelos entrenados.
- Regresión usa una variable de entrada; MLP tiene una salida binaria. K-Means devuelve una tabla con cluster, no un modelo para predecir nuevos puntos.
- Las operaciones tabulares producen nuevas tablas, pero las estructuras internas Python no son profundamente inmutables. Hay reasignaciones y efectos de entrada/salida.
- Los nombres de variables y columnas usados en la sintaxis admiten letras ASCII, números y guion bajo; no pueden comenzar por número ni ser palabras reservadas. Los textos sí admiten tildes.
- No hay break, continue, diccionarios literales, asignación por índice ni interfaz interactiva REPL. Las cadenas usan comillas dobles y no tienen secuencias de escape.
- Las rutas de entrada y salida se usan desde la carpeta actual. Ejecuta desde la raíz del proyecto.
- El límite por defecto de 10000 iteraciones se aplica a cada ejecución de mientras. No constituye un aislamiento de seguridad para código no confiable.

## Aclaraciones frente a la guía anterior
El atributo real de Matriz es filas_datos; el diccionario de símbolos se llama _simbolos; la pila local se llama _marcos_locales. ANTLR produce aquí un árbol de análisis sintáctico que se interpreta directamente, sin una fase separada de AST propio. Matplotlib es externo y usa NumPy indirectamente. No se debe afirmar que todo el entorno carece de librerías externas ni que el lenguaje es estrictamente funcional.
