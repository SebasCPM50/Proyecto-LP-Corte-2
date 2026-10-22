# GUÍA COMPLETA DE ESTUDIO Y SUSTENTACIÓN — SEGUNDO CORTE
# PROYECTO: ARCANUM (DSL DE CIENCIA DE DATOS)
# ASIGNATURA: LENGUAJES DE PROGRAMACIÓN Y TRANSDUCCIÓN
# DOCENTE: JOAQUÍN F. SÁNCHEZ

---

## 1. ¿EL LENGUAJE HACE FOR Y WHILE? (IMPLÍCITA Y EXPLÍCITAMENTE)

### La respuesta conceptual (Lo que debes responderle al profesor):
> "Profesor, en la sintaxis de Arcanum el usuario no escribe ciclos `for` o `while` porque es un **DSL declarativo de ciencia de datos**, no un lenguaje imperativo de propósito general como C o Python.  
> En ciencia de datos (exactamente igual que en **SQL** con `SELECT...WHERE` o en **R** con `dplyr`), el analista expresa **QUÉ** transformación desea realizar, no **CÓMO** iterar.  
> Por debajo, nuestro motor artesanal ejecuta ciclos `for` internos para procesar cada fila. Y a nivel del lenguaje, la repetición algorítmica se logra mediante **recursión en las recetas**."

### ¿Dónde se hacen ciclos por debajo en el código?
Aunque el usuario no escriba `for` en su archivo `.arc`, el intérprete ejecuta ciclos `for` nativos en Python en cada una de estas operaciones:
1. **En el filtrado (`purificar`)**: Recorre la lista de filas con un ciclo `for fila in self.filas:` y evalúa la condición booleana para cada una.
2. **En las columnas calculadas (`transmutar`)**: Recorre las filas con `for fila in self.filas:` y calcula la fórmula matemática fila por fila.
3. **En la sanación de nulos (`sanar`)**: Itera sobre las filas con `for fila in self.filas:` verificando si alguna columna contiene valores vacíos.
4. **En el agrupamiento (`destilar`)**: Itera sobre todas las filas con un ciclo `for` para clasificarlas en cubos (grupos) según la clave de agrupación.
5. **En la carga de archivos (`Pocion.desde_csv`)**: Recorre con `for linea in lineas:` cada renglón del texto para convertirlo en diccionarios.
6. **En la visualización (`mostrar`)**: Recorre la tabla con un `for` para imprimir cada fila alineada en la terminal.

### ¿Se pueden hacer repeticiones en el lenguaje Arcanum?
Sí, mediante **recursión en las recetas (funciones propias)**.  
Por ejemplo, una receta para calcular factorial o una suma repetitiva:
```arc
receta cuenta_regresiva(n) {
    # Una receta puede llamarse a sí misma de manera recursiva
    devolver n;
}
```

---

## 2. CÓMO FUNCIONA LA CARGA Y LECTURA DE ARCHIVOS CSV

### ¿Qué hace el código por debajo paso a paso?
El método encargado de esto es `Pocion.desde_csv(ruta)` en `src/pocion.py`:

```
Archivo en disco (.csv)
        │
        ▼ (1. open con encoding utf-8)
Lectura de líneas en memoria (.readlines)
        │
        ▼ (2. primera línea .split(","))
Cabecera: ['fecha', 'ciudad', 'precio']
        │
        ▼ (3. líneas siguientes .split(","))
Conversión de tipos celda por celda (_convertir_tipo_dato)
   - "" o "NaN"  --> None
   - "verdadero" --> True
   - "3"         --> int(3)
   - "150.5"     --> float(150.5)
   - "Bogota"    --> str("Bogota")
        │
        ▼ (4. emparejar columna con valor)
Fila en diccionario: {'fecha': '2026-01-05', 'ciudad': 'Bogota', 'precio': 150000}
        │
        ▼ (5. agregar a lista de filas)
Objeto Pocion(columnas, filas)
        │
        ▼ (6. registrar en Tabla de Símbolos)
Memoria del Intérprete
```

### Qué decirle al profesor sobre la carga de CSV:
> "Profesor, no utilizamos la librería Pandas ni el módulo csv de Python.  
> Diseñamos nuestro propio lector de texto plano:  
> 1. Abrimos el archivo físico con la función nativa `open()`.  
> 2. Leemos la primera línea y la cortamos por comas con `.split(',')` para extraer los nombres de los ingredientes (columnas).  
> 3. Recorremos los renglones siguientes e implementamos una función propia de inferencia de tipos (`_convertir_tipo_dato`) que detecta automáticamente si una celda es un número entero (`int`), decimal (`float`), booleano (`bool`), texto limpio o valor nulo (`None`).  
> 4. Cada registro se estructura como un diccionario clave-valor y se almacena en la lista de filas de nuestra clase `Pocion`, registrándose inmediatamente en la Tabla de Símbolos."

---

## 3. EXPLICACIÓN DETALLADA DE LOS CÓDIGOS IMPORTANTES

### A. `src/pocion.py` (La estructura de datos tabular artesanal)
Es el núcleo del proyecto. Reemplaza a Pandas desde cero.

* **`_convertir_tipo_dato(texto)`**:  
  Función utilitaria que recibe una cadena de texto cruda extraída del CSV y la parsea a su tipo de Python adecuado: si está vacía retorna `None`, si es número entero ejecuta `int()`, si tiene punto decimal ejecuta `float()`, y si es texto elimina comillas externas.
* **`Pocion.__init__(self, columnas, filas)`**:  
  Constructor. Recibe la lista de columnas y la lista de filas. Realiza copias independientes de cada diccionario (`dict(f)`) para garantizar que las modificaciones nunca alteren otras pociones (inmutabilidad).
* **`Pocion.desde_csv(ruta)`**:  
  Lee el archivo CSV del disco, parsea la cabecera y llena la lista de diccionarios de filas.
* **`Pocion.a_csv(ruta)`**:  
  Exporta la tabla a un archivo CSV físico. Escribe primero la cabecera separada por comas y luego cada fila iterando sobre los valores.
* **`Pocion.recolectar(lista_columnas)`**:  
  Implementa la proyección (selección de columnas). Crea diccionarios nuevos que contienen únicamente las claves solicitadas por el usuario.
* **`Pocion.purificar(evaluador_condicion)`**:  
  Implementa el filtrado de filas. Recorre las filas y ejecuta la función de condición; solo las filas que retornen `True` pasan a la nueva Poción.
* **`Pocion.ordenar(columna, ascendente)`**:  
  Ordena las filas usando `sorted()`. Cuenta con una función de clave inteligente que coloca los valores `None` de forma segura al final para evitar errores de comparación entre tipos incompatibles.
* **`Pocion.transmutar(nombre_columna, evaluador_expresion)`**:  
  Crea una columna calculada. Itera fila por fila, evalúa la expresión aritmética para esa fila y almacena el resultado bajo la nueva clave de columna.
* **`Pocion.sanar_descartar_nulos()`**:  
  Filtra y descarta cualquier fila que tenga al menos un valor `None` o vacío en cualquiera de sus columnas.
* **`Pocion.sanar_llenar_nulos(columna, valor_relleno)`**:  
  Recorre las filas y, si en la columna indicada el valor es `None`, lo sustituye por el `valor_relleno`.
* **`Pocion.destilar(columnas_grupo, lista_agregaciones)`**:  
  Agrupa las filas mediante un diccionario hash donde la clave es la tupla de los valores agrupadores. Luego calcula matemáticamente:
  - `suma`: usa `sum(valores)`
  - `media`: divide `sum(valores) / len(valores)`
  - `mediana`: ordena los números del grupo y toma el del centro
  - `minimo` y `maximo`: usa `min()` y `max()`
  - `desviacion`: calcula la raíz cuadrada de la varianza muestral $\sqrt{\frac{\sum (x - \bar{x})^2}{n - 1}}$
  - `contar`: cuenta la cantidad de registros del grupo
* **`Pocion.describir()`**:  
  Calcula una tabla resumen de estadísticas para todas las columnas numéricas de la poción.
* **`Pocion.mostrar()`**:  
  Formatea e imprime en la consola la tabla completa sin omitir filas, calculando dinámicamente el ancho de cada columna para que quede alineada sin necesidad de librerías externas.

---

### B. `src/tabla_simbolos.py` (La libreta de memoria)

* **`class Simbolo`**:  
  Representa una variable. Guarda:
  - `nombre`: identificador (ej. `"ventas"`).
  - `tipo`: categoría semántica (`"POCION"`, `"NUMERO"`, `"CADENA"`, `"BOOLEANO"`).
  - `valor`: el objeto real almacenado (ej. la instancia de `Pocion` o el número flotante).
  - `linea` y `columna`: ubicación en el archivo `.arc` donde se definió.
* **`TablaSimbolos.__init__()`**:  
  Inicializa el diccionario `self._simbolos = {}`.
* **`definir(nombre, valor)`**:  
  Determina el tipo del valor y lo almacena en el diccionario.
* **`obtener(nombre)`**:  
  Busca la variable en el diccionario. Si no existe, lanza un `ErrorSemantico` informando la línea y columna exactas.
* **`obtener_pocion(nombre)`**:  
  Recupera la variable y además comprueba que sea de tipo `POCION`. Si el usuario intenta hacer una operación de tabla sobre un número, lanza un error semántico explicativo.
* **`verificar_columna(nombre_pocion, nombre_columna)`**:  
  Comprueba que la columna exista dentro de la lista `pocion.columnas`. Si no existe, lanza un error semántico y lista las columnas que sí están disponibles.
* **`imprimir()`**:  
  Imprime en consola el resumen de todas las variables guardadas en memoria al finalizar el programa.

---

### C. `src/errores.py` (Manejo amigable de fallos)

* **`class ErrorSemantico(Exception)`**:  
  Excepción propia que guarda el mensaje de error, la línea y la columna. Su método `__str__` formatea el error en español:  
  `[Error Semántico] Línea X, Columna Y: mensaje`.
* **`class ManejadorErrores(ErrorListener)`**:  
  Hereda del `ErrorListener` de ANTLR. Reemplaza los mensajes técnicos en inglés de ANTLR por mensajes limpios en español cuando hay tokens inesperados o caracteres inválidos.

---

### D. `src/main.py` (Punto de entrada y orquestador)

* **`imprimir_arbol(nodo, parser, sangria)`**:  
  Función recursiva que recorre el árbol sintáctico (AST) de ANTLR e imprime su estructura jerárquica con sangrías si se pasa la bandera `--arbol`.
* **`ejecutar(ruta_archivo, mostrar_arbol)`**:  
  Orquesta las fases del compilador en secuencia:
  1. Abre el archivo con `FileStream`.
  2. Inicializa el `ArcanumLexer` para separar el texto en tokens.
  3. Pasa los tokens al `ArcanumParser` para verificar la gramática.
  4. Si hay errores léxicos o sintácticos, los imprime y detiene la ejecución.
  5. Si la sintaxis es válida, crea una nueva `TablaSimbolos()`.
  6. Instancia el `ArcanumVisitorEjecutor(tabla)`.
  7. Llama a `visitor.visit(arbol)` para ejecutar el código.
  8. Captura cualquier `ErrorSemantico` y lo muestra limpiamente en pantalla.

---

### E. `src/visitor.py` (El motor de ejecución - Patrón Visitor)

Hereda de `ArcanumVisitor` generado por ANTLR y contiene un método `visit...` por cada regla de la gramática:

* **`visitPrograma` y `visitHechizo`**: Recorren secuencialmente cada instrucción del archivo.
* **`visitAsignacion`**: Evalúa la expresión a la derecha del `=` y guarda el resultado en la Tabla de Símbolos.
* **`visitInvocarExpr`**: Extrae la ruta entre comillas y llama a `Pocion.desde_csv()`.
* **`visitRecolectarExpr`**: Valida que las columnas existan y llama a `pocion.recolectar()`.
* **`visitPurificarExpr`**: Establece temporalmente `self._fila_activa = fila` y evalúa la condición para cada registro llamando a `pocion.purificar()`.
* **`visitOrdenarExpr`**: Revisa si el usuario escribió `asc` o `desc` y llama a `pocion.ordenar()`.
* **`visitTransmutarExpr`**: Establece `self._fila_activa = fila`, evalúa la expresión aritmética para cada registro y llama a `pocion.transmutar()`.
* **`visitSanarExpr`**: Revisa si la orden es `descartar_nulos` o `llenar` y ejecuta la limpieza correspondiente.
* **`visitDestilarExpr`**: Extrae las columnas de agrupación y la lista de funciones (`suma`, `media`, `contar`) y llama a `pocion.destilar()`.
* **`visitInstruccionRevelar` y `visitInstruccionDescribir`**: Obtienen la poción de la tabla de símbolos y llaman a `.mostrar()`.
* **`visitInstruccionPreservar`**: Llama a `.a_csv()` para guardar la tabla en disco.
* **`visitInstruccionUsar`**: Lee un archivo de compendio (ej. `compendios/matematicas.arc`), lo parsea con ANTLR y registra sus funciones en `self._compendios`.
* **`visitDefinicionReceta` y `visitLlamadaReceta`**: Permiten registrar y ejecutar funciones propias. Al invocar una receta, crea un marco local (`marco_local = dict(...)`) en una pila `self._marcos_locales` para aislar los argumentos locales de las variables globales.
* **`visitIdentificador`**: Resuelve qué significa una variable buscando en orden de prioridad:
  1. En los parámetros locales de la receta actual (si estamos dentro de una función).
  2. En las columnas de la fila actual (si estamos dentro de un filtro o columna calculada).
  3. En la Tabla de Símbolos global.

---

## 4. ESTRUCTURAS DE DATOS USADAS A PROFUNDIDAD

En este proyecto se aplican cinco estructuras de datos clásicas de las ciencias de la computación:

### 1. Lista de Diccionarios (`List[Dict[str, Any]]`) — Representación Tabular
* **Concepto**: Una tabla bidimensional donde cada fila es una tabla hash (`dict`) y toda la colección es un arreglo dinámico (`list`).
* **Complejidad algorítmica**:
  - Acceso a un campo de una fila (`fila['precio']`): $\mathcal{O}(1)$ tiempo constante.
  - Recorrido completo de la tabla: $\mathcal{O}(N)$ tiempo lineal.
* **Por qué se eligió**: A diferencia de una matriz de listas (`List[List]`) donde tienes que recordar que la columna 3 es el precio, el diccionario permite indexar por el nombre del ingrediente (`fila['precio']`), haciendo el código intuitivo y evitando desalineaciones al eliminar o agregar columnas.

### 2. Tabla Hash (`Dict[str, Simbolo]`) — Tabla de Símbolos
* **Concepto**: Mapeo asociativo que asocia cadenas de texto (identificadores) con registros semánticos (`Simbolo`).
* **Complejidad algorítmica**:
  - Inserción de variable (`definir`): $\mathcal{O}(1)$ promedio.
  - Búsqueda de variable (`obtener`): $\mathcal{O}(1)$ promedio.
* **Por qué se eligió**: Garantiza que el compilador no pierda tiempo buscando variables secuencialmente, permitiendo verificar existencias y tipos de forma instantánea.

### 3. Árbol n-ario Jerárquico — Árbol de Análisis Sintáctico (AST)
* **Concepto**: Árbol donde cada nodo interno es una regla sintáctica y las hojas son los tokens terminales.
* **Por qué se eligió**: Modela naturalmente la precedencia matemática. Por ejemplo, en `subtotal - (subtotal * descuento)`, la multiplicación queda en un subárbol más profundo que la resta, garantizando que el Visitor evalúe primero las operaciones de mayor prioridad.

### 4. Hash Map de Agrupación Multivariable (`Dict[Tuple, List[Dict]]`)
* **Concepto**: En el método `destilar()`, se utiliza un diccionario donde la clave es una tupla con los valores de las columnas agrupadoras (ej. `('Bogota', 'Electronica')`) y el valor es la lista de filas que comparten esa clave.
* **Complejidad algorítmica**: Permite clasificar $N$ registros en sus grupos correspondientes en una sola pasada de tiempo lineal $\mathcal{O}(N)$, sin necesidad de ordenar previamente la tabla ($\mathcal{O}(N \log N)$).

### 5. Pila de Llamadas y Ámbitos (`Call Stack / List[Dict]`)
* **Concepto**: Estructura LIFO (Last In, First Out) en `self._marcos_locales`.
* **Por qué se eligió**: Permite que las recetas tengan variables y parámetros locales independientes. Al llamar a una receta se hace `push` (con `.append()`) y al terminar se hace `pop()` (con `.pop()`), garantizando que los parámetros locales no sobreescriban ni ensucien las variables globales.
