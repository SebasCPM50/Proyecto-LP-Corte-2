# Documento de Reglas Semánticas — Arcanum
**Curso:** Lenguajes de Programación y Transducción — Semestre 2026-2  
**Corte Actual:** 2 — Semántica y procesamiento de datos  
**Temática:** Alquimia aplicada a la ciencia de datos  
**Requisito Crucial:** 100% CERO LIBRERÍAS EXTERNAS (Sin Pandas, Sin NumPy). Estructuras artesanales construidas desde cero.

---

## 1. Introducción y Enfoque Artesanal

En este Segundo Corte, **Arcanum no utiliza ninguna librería externa de ciencia de datos** (ni Pandas, ni NumPy, ni módulos externos de cálculo). Todo el motor de datos y el sistema de módulos fue desarrollado desde cero en Python estándar utilizando exclusivamente listas, diccionarios y operaciones aritméticas nativas.

El análisis semántico garantiza:
1. Que no se utilicen variables que no hayan sido declaradas.
2. Que las operaciones tabulares se apliquen exclusivamente sobre objetos de tipo `POCION`.
3. Que las columnas (ingredientes) referenciadas existan en la cabecera de la poción.
4. Que no ocurran divisiones por cero ni operaciones entre tipos incompatibles.
5. Que las funciones propias del lenguaje (**recetas**) y las librerías reutilizables (**compendios**) se resuelvan de forma aislada, sin depender del `import` de Python.

---

## 2. Sistema de Tipos Nativos de Arcanum

| Tipo Semántico | Descripción | Implementación Interna en Python | Ejemplo en Arcanum |
|---|---|---|---|
| **`POCION`** | Estructura de datos tabular artesanal. | Clase `Pocion` (`src/pocion.py`): lista de columnas + lista de diccionarios | `ventas = invocar desde "csv/ventas.csv";` |
| **`NUMERO`** | Valor numérico escalar (entero o punto flotante). | `int` o `float` nativo | `tasa = 0.19;` o `unidades = 5;` |
| **`CADENA`** | Secuencia de texto alfanumérico. | `str` nativo | `ciudad = "Bogota";` |
| **`BOOLEANO`** | Valor de verdad lógico (`verdadero` o `falso`). | `bool` nativo | `activo = verdadero;` |

---

## 3. Estructura Interna de la Poción (Reemplazo de Pandas)

La clase `Pocion` en `src/pocion.py` almacena los datos de la forma más pedagógica y limpia posible:
- **`self.columnas`**: Lista con los nombres de las columnas, por ejemplo `['fecha', 'ciudad', 'precio']`.
- **`self.filas`**: Lista de diccionarios donde cada elemento es una fila, por ejemplo `[{'fecha': '2026-01-05', 'ciudad': 'Bogota', 'precio': 150000}, ...]`.

Al **purificar** (filtrar), se recorre la lista de filas con un ciclo nativo y se conservan únicamente aquellas que cumplen la condición.  
Al **transmutar** (columna calculada), se calcula la expresión para cada diccionario y se añade la nueva clave.  
Al **destilar** (agrupar), se agrupan las filas en un diccionario `{clave_grupo: [filas]}` y se calculan las sumas, medias y conteos con matemáticas puras de Python.

---

## 4. Reglas Semánticas Formales

### Regla 1: Declaración Previa Obligatoria
- Una variable debe haber sido asignada previamente antes de ser leída.
- Si no existe en la Tabla de Símbolos (ni en el marco de parámetros locales si estamos dentro de una receta), se detiene con:
  ```text
  [Error Semántico] Línea X, Columna Y: La variable o ingrediente 'nombre' no ha sido declarada o invocada previamente.
  ```

### Regla 2: Coherencia de Tipos en Operaciones Tabulares
- Instrucciones como `recolectar`, `purificar`, `ordenar`, `transmutar`, `sanar`, `destilar`, `preservar`, `revelar` y `describir` requieren obligatoriamente una variable de tipo `POCION`.
- Si se intenta operar sobre un número o texto:
  ```text
  [Error Semántico] Línea X, Columna Y: La variable 'descuento' es de tipo NUMERO, no es una POCIÓN (tabla de datos).
  ```

### Regla 3: Validación de Ingredientes (Columnas)
- Antes de seleccionar, filtrar, transmutar o agrupar, se comprueba que el nombre de la columna esté en `pocion.columnas`.
- Si no está, se informa el error y se listan las columnas disponibles.

### Regla 4: Incompatibilidad Aritmética y División por Cero
- Operaciones como `*`, `/`, `%`, `-`, `^` exigen operandos numéricos.
- La división por cero genera un error semántico explícito:
  ```text
  [Error Semántico] Línea X, Columna Y: División por cero no permitida.
  ```

### Regla 5: Resolución de Compendios y Recetas (Librerías Propias)
- La instrucción `usar compendio <nombre>;` busca un archivo en `compendios/<nombre>.arc`.
- El archivo se procesa con el propio analizador de Arcanum y sus recetas se registran en la tabla de compendios sin invocar ningún `import` de Python.
- Las llamadas a recetas (`compendio.receta(args)`) crean un marco local de variables para aislar sus parámetros del entorno global.

---

## 5. Patrones de Diseño Utilizados

1. **Patrón Visitor**: Recorre los nodos del árbol sintáctico generado por ANTLR y ejecuta la semántica correspondiente sin ensuciar la gramática.
2. **Patrón Tabla de Símbolos**: Libreta de memoria central que rastrea nombres, tipos y valores de variables.
3. **Patrón Fachada (`MotorDatos`)**: Interfaz sencilla que delega las transformaciones a la clase artesanal `Pocion`.
