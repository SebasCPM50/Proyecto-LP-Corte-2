# GUÍA MAESTRA DE SUSTENTACIÓN ORAL — PROFESOR JOAQUÍN F. SÁNCHEZ
# ANÁLISIS DEL AUDIO DE SUSTENTACIÓN REAL + ESTRATEGIA DEFENSIVA ARCANUM
# ASIGNATURA: LENGUAJES DE PROGRAMACIÓN Y TRANSDUCCIÓN
# UNIVERSIDAD SERGIO ARBOLEDA

Esta guía fue elaborada analizando minuciosamente la sustentación real de tus compañeros (Brian, David y Laura) con el profesor Joaquín F. Sánchez, combinando las preguntas sorpresa que él hace, sus pruebas en vivo en el computador y las preguntas teóricas que hace en hoja de papel.

---

## 1. RADIOGRAFÍA DE LA SUSTENTACIÓN REAL (LO QUE PASÓ EN EL AUDIO)

El profesor Joaquín tiene una metodología de evaluación muy definida dividida en tres momentos:

### Momento 1: Revisión del script y del código Python por debajo
* Pide ver el script `.arc` y el código fuente en Python al mismo tiempo
* Pregunta por qué se hace copia de datos (`datos_limpios = datos_crudos`) y ataca el tema del consumo de memoria RAM
* Exige que el alumno explique la sintaxis exacta de Python que usó (a tus compañeros los corchó preguntándoles qué significaban los dos puntos `filas: list = []` y cómo funcionaba su estructura interna)

### Momento 2: La prueba de fuego en vivo (Modificación del CSV)
* El profesor abre directamente el archivo CSV (en el audio abrió `ventas.csv`), **borra filas en vivo**, lo guarda y dice: *"Vete al programa y ejecútalo ya mismo"*
* Lo hace para verificar si los resultados se adaptan dinámicamente o si los estudiantes dejaron datos "quemados" (hardcodeados) en el código

### Momento 3: Las preguntas de funcionalidad faltante
* Pregunta: *"¿Sus bibliotecas las manejan ustedes solos? ¿Seguros? ¿Tienen aleatorio? ¿El poder generar un random?"* (A tus compañeros les bajó la nota por no tener random)
* Pregunta: *"¿Manejan for o while? ¿Si yo necesito hacer un for o un while para un pequeño programa no lo puedo hacer?"*

### Momento 4: Las preguntas teóricas en hoja de papel
* Pide una hoja y lápiz para que escriban a mano:
  1. ¿Qué es una derivación por la derecha y un ejemplo de regla de producción?
  2. ¿Para qué sirve el símbolo de pesos (`$`) en compiladores?
  3. ¿Por qué el conjunto de Siguientes (`Follow`) NUNCA puede llevar vacío ($\epsilon$)?

---

## 2. CÓMO RESPONDER CADA PREGUNTA DEL PROFESOR EN ARCANUM

### Pregunta 1: "¿Por qué hacen copias de datos y cuánta memoria gasta eso?"
**Lo que pasó en el audio:** El grupo dijo que hacían copias para no dañar el original, y el profe les dijo: *"Si el archivo pesa 500 MB, van a tener 1000 MB en memoria... muy ineficiente"*.

**Cómo debes responder tú en Arcanum:**
> *"Profesor, en nuestro diseño aplicamos el **Principio de Inmutabilidad** propio de los lenguajes analíticos modernos como R, Scala o Apache Spark.  
> Cada transformación genera una Poción nueva para evitar efectos colaterales (side-effects) en pipelines de análisis.  
> Respecto a la memoria:  
> 1. En Python, los diccionarios de cada fila contienen referencias a los mismos objetos inmutables en memoria (cadenas y números), no duplicamos los datos atómicos crudos.  
> 2. Además, cuando una variable deja de referenciarse en el script, el recolector de basura (Garbage Collector) de Python libera la memoria automáticamente.  
> Es un equilibrio deliberado entre seguridad e integridad analítica frente a mutabilidad destructiva."*

---

### Pregunta 2: "¿Tienen aleatorio? ¿Pueden generar un random?"
**Lo que pasó en el audio:** El profe les preguntó si tenían números al azar y no tenían. Les dijo: *"No tienen aleatorio... bueno listo, es que tenían que agregarlo"*.

**Cómo debes responder tú en Arcanum (¡ESTA ES TU GRAN VENTAJA!):**
> *"Sí, profesor. Arcanum cuenta con generación de azar 100% artesanal sin usar la librería `random` de Python:  
> 1. Implementamos un **Generador Congruencial Lineal (LCG)** desde cero en `pocion.py`.  
> 2. El analista puede invocar `random()` para decimales entre 0 y 1, `random(100)` para enteros hasta 100, o `random(1, 6)` para simular un dado.  
> 3. También creamos la receta `matematicas.random(semilla, inicio, fin)` en nuestro compendio propio.  
> 4. Y a nivel de datos tabulares, implementamos el algoritmo de **Fisher-Yates** a mano en `pocion.muestra_aleatoria(n)` para extraer muestras sin reemplazo."*
*(Abres el archivo `compendios/matematicas.arc` o corres un ejemplo con `random(1, 6)` en la terminal).*

---

### Pregunta 3: "¿Tienen for y while? ¿Si yo necesito hacer un ciclo cómo lo hago?"
**Lo que pasó en el audio:** El profe se molestó porque los alumnos dijeron que como era un pipeline no necesitaban ciclos y que la gramática no lo soportaba. Les dijo: *"Todo, todo es un lenguaje de programación... si necesito hacer un pequeño programa para hacer algo, ¿no tendría la capacidad?"*.

**Cómo debes responder tú en Arcanum:**
> *"Profesor, en Arcanum los ciclos se manejan en dos niveles:  
> 1. **A nivel de datos tabulares**, Arcanum es un DSL declarativo orientado a pipelines (como SQL o dplyr en R), por lo que las operaciones sobre filas (`purificar`, `transmutar`, `destilar`) aplican ciclos `for` internos vectorizados para que el usuario no tenga que iterar manualmente.  
> 2. **A nivel de control algorítmico del lenguaje**, Arcanum soporta **recursión en recetas**. En ciencias de la computación y programación funcional, cualquier ciclo `for` o `while` se expresa de manera formal mediante recursión de cola."*

**Si el profesor te dice: "A ver, hágame un ciclo repetitivo aquí mismo":**  
Le muestras o escribes una receta recursiva:
```arc
receta repetir(contador, limite) {
    revelar contador;
    si (contador < limite) {
        devolver repetir(contador + 1, limite);
    }
    devolver contador;
}

fin = repetir(1, 5);
```

---

### Pregunta 4: "¿Tienen funciones implícitas o usan librerías como en Python?"
**Lo que pasó en el audio:** El profe criticó que el otro grupo tenía funciones como `eliminar_duplicados` metidas a la fuerza en el script sin importarlas de ningún lado: *"En Python tienes que decirle `import math`... ¿eliminar duplicados está siempre presente consumiendo memoria?"*.

**Cómo debes responder tú en Arcanum:**
> *"Profesor, en Arcanum las funciones no están cargadas a la fuerza ni consumiendo memoria innecesariamente.  
> Diseñamos un sistema formal de **Compendios** (librerías propias en archivos `.arc`).  
> Si el analista necesita funciones matemáticas o estadísticas, debe cargarlas explícitamente con `usar compendio matematicas;` o `usar compendio estadistica;`.  
> De esa forma la memoria solo reserva las recetas que el programa realmente necesita."*

---

### Pregunta 5: La prueba de modificar el CSV en vivo
**Lo que va a hacer el profesor:**  
Va a abrir `csv/ventas.csv` con un editor de texto, va a borrar filas o dejar solo 2 registros, va a guardar el archivo y te va a decir: *"Ejecútalo ya"*.

**Por qué Arcanum es invencible en esta prueba:**  
Nuestro método `Pocion.desde_csv()` lee dinámicamente con `open().readlines()`. No tiene ninguna dimensión fija.  
Al correr:
```bash
python3 src/main.py examples/ejemplo1_analisis_ventas.arc
```
La terminal mostrará automáticamente:
`[Hechizo Invocado]: Poción cargada desde 'csv/ventas.csv' (2 registros)`  
Y todos los filtros, subtotales y agrupamientos se recalcularán exactamente sobre esos 2 registros sin romperse.

---

## 3. EL EXAMEN TEÓRICO EN HOJA DE PAPEL (PREGUNTAS DE GRAMÁTICA)

En el audio, el profesor puso a los estudiantes a escribir en una hoja. Estas son las respuestas exactas que debes dominar:

---

### Tema A: ¿Qué es una derivación por la derecha (Rightmost Derivation)?

#### Definición exacta para decirle:
> *"Una **derivación por la derecha** (o derivación canónica por la derecha) es aquella en la que en cada paso de reemplazo se sustituye siempre el símbolo **no terminal que se encuentra más a la derecha** en la forma de frase actual."*

#### Ejemplo práctico para escribirle en la hoja:
Dada la gramática sencilla de expresiones:
$$E \rightarrow E + T \mid T$$
$$T \rightarrow T * F \mid F$$
$$F \rightarrow \text{id}$$

Para derivar la cadena $\text{id} + \text{id} * \text{id}$ **por la derecha**:
1. $E$
2. $\Rightarrow E + T$ *(reemplazamos el no terminal más a la derecha, que es $T$)*
3. $\Rightarrow E + T * F$ *(reemplazamos $F$)*
4. $\Rightarrow E + T * \text{id}$ *(reemplazamos $T$)*
5. $\Rightarrow E + F * \text{id}$ *(reemplazamos $F$)*
6. $\Rightarrow E + \text{id} * \text{id}$ *(reemplazamos $E$)*
7. $\Rightarrow T + \text{id} * \text{id}$ *(reemplazamos $T$)*
8. $\Rightarrow F + \text{id} * \text{id}$ *(reemplazamos $F$)*
9. $\Rightarrow \text{id} + \text{id} * \text{id}$

*(Dile: "Profesor, los analizadores sintácticos ascendentes tipo LR o LALR, como los que usa internamente ANTLR o Yacc, construyen el árbol reconociendo el inverso de una derivación por la derecha").*

---

### Tema B: ¿Para qué sirve el símbolo de pesos (`$`)?

#### Lo que contestó la compañera (MAL):
Dijo que era *"para las predicciones"*, y el profesor le gritó: *"¡Nooo! Eso no es"*.

#### La respuesta correcta:
> *"El símbolo `$` es el **marcador especial de fin de entrada** (End of Input / End of File).  
> Representa que se ha llegado al final de la cadena de tokens analizada. En los autómatas de pila de los analizadores sintácticos (como LL o LR), se coloca en el fondo de la pila y al final de la cadena de entrada para verificar que la aceptación del programa sea exitosa cuando la pila queda vacía o en el estado de aceptación final."*

---

### Tema C: ¿Por qué Siguientes (`Follow`) NUNCA puede llevar vacío ($\epsilon$)?

#### La explicación conceptual:
> *"El conjunto **$Siguiente(A)$** se define formalmente como el conjunto de símbolos terminales que pueden aparecer **inmediatamente a la derecha** de $A$ en alguna forma de frase derivada del símbolo inicial ($S \Rightarrow^* \alpha A a \beta$).  
> 
> $\epsilon$ (épsilon) **no es un símbolo terminal ni un token real**; representa la ausencia de símbolo o la cadena vacía.  
> Cuando una variable $A$ está al final de una cadena y ya no hay ningún símbolo detrás de ella, lo que le sigue formalmente es el marcador de fin de archivo `$`, **nunca $\epsilon$**.  
> Por definición matemática, $Siguiente(A) \subseteq \Sigma \cup \{\$\}$, donde $\Sigma$ son los terminales del lenguaje; por tanto, $\epsilon$ jamás puede pertenecer a $Siguiente$."*

---

### Tema D: Diferencia entre Primeros (`First`) y Siguientes (`Follow`)

| Propiedad | Conjunto Primeros (`First`) | Conjunto Siguientes (`Follow`) |
| :--- | :--- | :--- |
| **¿Qué contiene?** | Terminales con los que puede **comenzar** una cadena derivada de $\alpha$ | Terminales que pueden aparecer **después** de $A$ |
| **¿Puede contener $\epsilon$?** | **SÍ**, si la regla puede anularse ($A \rightarrow \epsilon$) | **NO**, bajo ninguna circunstancia |
| **Símbolo de fin (`$`)** | No suele contenerlo | **SÍ**, el símbolo inicial $S$ siempre contiene `$` |

---

## 4. CHECKLIST FINAL PARA ENTRAR A LA SUSTENTACIÓN

1. **Tener la máquina virtual con el proyecto abierto en la terminal:**
   ```bash
   cd ~/proyecto_lenguajes_segundo_corte
   source venv/bin/activate
   ```
2. **Correr pytest antes de que se siente el profesor para tenerlo listo:**
   ```bash
   python3 -m pytest tests/
   ```
   *(Mostrarle los 28 tests pasando en verde le da una primera impresión demoledora).*
3. **Saber abrir un script y ejecutarlo:**
   ```bash
   python3 src/main.py examples/ejemplo1_analisis_ventas.arc
   ```
4. **Si pide ver el árbol de derivación:**
   ```bash
   python3 src/main.py examples/ejemplo1_analisis_ventas.arc --arbol
   ```
5. **Si te pide el random:**
   Muéstrale `src/pocion.py` líneas de `_generar_siguiente_azar()` y `numero_aleatorio()`, o ejecuta `examples/ejemplo4_compendios_recetas.arc`.
6. **Si te altera el CSV:**
   No te pongas nervioso. Guárdalo y dale a la flecha arriba en la terminal para reejecutar. Arcanum lo procesará perfecto.


---

## 5. EXPLICACIÓN LÍNEA POR LÍNEA DE CADA CÓDIGO Y SUS MÉTODOS

Aquí tienes el desglose exacto de cada archivo y de cada método para que, si el profesor señala la pantalla y te pregunta *"¿Qué hace esta línea?"*, respondas con total seguridad.

---

### ARCHIVO 1: `src/pocion.py` (Estructura Tabular Artesanal)
Es el archivo más importante de todo el proyecto. Reemplaza a Pandas y NumPy desde cero.

#### Funciones auxiliares fuera de la clase:
* **`_convertir_tipo_dato(texto)`**:
  * **Qué hace:** Recibe el texto crudo de una celda del CSV y descubre qué tipo de dato es para convertirlo.
  * **Cómo funciona por dentro:** Limpia espacios con `.strip()`. Si está vacío o dice `"NAN"`, devuelve `None`. Si dice `"verdadero"` o `"true"`, devuelve `True`. Si dice `"falso"`, devuelve `False`. Luego intenta hacer `int(texto)`; si falla, intenta hacer `float(texto)`; y si tiene comillas a los lados, se las quita con `texto[1:-1]` y lo deja como cadena limpia.
  * **Qué decirle al profesor:** *"Es nuestro analizador léxico de celdas. Infiere dinámicamente si el dato es entero, flotante, booleano, texto o nulo sin usar librerías externas"*.
* **`_generar_siguiente_azar()`**:
  * **Qué hace:** Genera un número pseudoaleatorio utilizando un algoritmo congruencial lineal (LCG).
  * **Cómo funciona por dentro:** Aplica la fórmula matemática entera $X_{n+1} = (X_n \cdot 1103515245 + 12345) \pmod{2^{31}}$. La semilla se inicializa mezclando el `id()` de un objeto con el `os.getpid()` del proceso para que nunca empiece con el mismo valor.
  * **Qué decirle al profesor:** *"Es el algoritmo de Lehmer / Congruencial Lineal programado a mano para generar números al azar sin usar `import random`"*.
* **`numero_aleatorio(minimo=0, maximo=1)`**:
  * **Qué hace:** Devuelve un número al azar dentro del rango que le pidan.
  * **Cómo funciona por dentro:** Divide el azar crudo entre $2147483647.0$ para obtener un decimal entre 0 y 1. Si los argumentos son enteros (ej. `random(1, 6)`), calcula el rango `(maximo - minimo) + 1` y devuelve un entero. Si no le pasan nada, devuelve un flotante redondeado a 4 decimales.

#### Métodos de la clase `Pocion`:
* **`__init__(self, columnas, filas)`**:
  * **Qué hace:** Constructor de la tabla de datos.
  * **Cómo funciona por dentro:** Guarda la lista de columnas en `self.columnas`. En `self.filas` guarda copias independientes de cada diccionario (`[dict(f) for f in filas]`) para garantizar la inmutabilidad y evitar que cambios posteriores afecten a otras pociones.
* **`resolver_ruta(cls, ruta)`**:
  * **Qué hace:** Método de clase que busca inteligentemente el archivo CSV si el usuario escribió una ruta relativa (busca en la carpeta actual, en `csv/`, en `datos/` o en `../csv/`).
* **`desde_csv(cls, ruta)`**:
  * **Qué hace:** Carga un archivo CSV desde el disco a la memoria.
  * **Cómo funciona por dentro:** Abre el archivo con `open(ruta, mode='r', encoding='utf-8')`. Lee las líneas con `.readlines()`. La primera línea la corta por comas con `.split(',')` para obtener las columnas. Para cada una de las líneas siguientes, corta por comas, pasa cada celda por `_convertir_tipo_dato()` y arma un diccionario clave-valor. Devuelve una instancia nueva de `Pocion(cabecera, filas)`.
* **`a_csv(self, ruta)`**:
  * **Qué hace:** Guarda la poción actual en un archivo CSV en disco.
  * **Cómo funciona por dentro:** Abre el archivo destino en modo escritura (`mode='w'`). Escribe primero las columnas separadas por coma (`",".join(self.columnas) + "\n"`). Luego recorre `self.filas` y escribe cada registro convirtiendo `None` en texto vacío.
* **`recolectar(self, lista_columnas)`**:
  * **Qué hace:** Proyección (selecciona columnas).
  * **Cómo funciona por dentro:** Recorre las filas y construye diccionarios nuevos que contienen únicamente las claves que están en `lista_columnas`. Devuelve una nueva `Pocion` con esas columnas.
* **`purificar(self, evaluador_condicion)`**:
  * **Qué hace:** Filtra las filas de la tabla según un predicado lógico.
  * **Cómo funciona por dentro:** Itera con `for fila in self.filas` y le pasa cada fila a la función booleana `evaluador_condicion(f)`. Solo las filas que dan `True` pasan a la nueva `Pocion`.
* **`ordenar(self, columna, ascendente=True)`**:
  * **Qué hace:** Ordena los registros según el valor de una columna.
  * **Cómo funciona por dentro:** Usa la función nativa `sorted()` con una función clave `clave_orden(fila)`. Si el valor es `None`, devuelve `(1, 0)`; si no, devuelve `(0, v)`. Esta técnica garantiza que los valores nulos siempre queden al final de forma segura sin generar errores de tipo entre números y `None`.
* **`transmutar(self, nombre_columna, evaluador_expresion)`**:
  * **Qué hace:** Agrega una columna calculada fila por fila.
  * **Cómo funciona por dentro:** Agrega `nombre_columna` a la lista de columnas. Luego recorre cada fila, calcula el nuevo valor evaluando la fórmula matemática sobre esa fila con `evaluador_expresion(fila)`, y guarda el resultado bajo la nueva clave del diccionario.
* **`sanar_descartar_nulos(self)`**:
  * **Qué hace:** Limpia la tabla descartando filas incompletas.
  * **Cómo funciona por dentro:** Revisa cada fila con `any(fila.get(c) is None for c in self.columnas)`. Si ninguna celda es `None`, la fila se conserva.
* **`sanar_llenar_nulos(self, columna, valor_relleno)`**:
  * **Qué hace:** Imputa valores por defecto en celdas vacías de una columna.
  * **Cómo funciona por dentro:** Recorre las filas y, si `fila.get(columna) is None`, le asigna `valor_relleno`.
* **`destilar(self, columnas_grupo, lista_agregaciones)`**:
  * **Qué hace:** Agrupamiento y agregación estadística (equivalente a `GROUP BY`).
  * **Cómo funciona por dentro:** Usa una tabla hash (`grupos = {}`) donde la clave es una tupla con los valores agrupadores `tuple(fila.get(col) for col in columnas_grupo)`. Clasifica todas las filas en sus grupos en una sola pasada $\mathcal{O}(N)$. Luego recorre cada grupo y calcula matemáticamente las agregaciones solicitadas (`suma`, `media`, `mediana`, `desviacion`, `minimo`, `maximo`, `contar`).
* **`describir(self)`**:
  * **Qué hace:** Genera la tabla resumen de estadísticas descriptivas.
  * **Cómo funciona por dentro:** Detecta cuáles columnas contienen números. Luego calcula para cada una de ellas: conteo, media, desviación estándar muestral ($\sqrt{\frac{\sum (x - \bar{x})^2}{n - 1}}$), mínimo y máximo. Devuelve una nueva Poción con las métricas en filas.
* **`mostrar(self)`**:
  * **Qué hace:** Imprime la tabla completa en consola alineada y sin recortar registros.
  * **Cómo funciona por dentro:** Mide el texto más largo de cada columna (`max_len`) para calcular el ancho de separación (`ljust(anchos[col])`). Muestra los valores `None` explícitamente para que el usuario vea dónde faltan datos.
* **`muestra_aleatoria(self, cantidad)`**:
  * **Qué hace:** Extrae un subconjunto de filas al azar sin reemplazo.
  * **Cómo funciona por dentro:** Aplica el algoritmo de mezcla de Fisher-Yates sobre los índices de la tabla usando `_generar_siguiente_azar()` y devuelve una nueva `Pocion` con las filas mezcladas.

---

### ARCHIVO 2: `src/tabla_simbolos.py` (Memoria del Compilador)
Maneja las variables, sus tipos semánticos y valida que las operaciones tengan sentido.

* **`class Simbolo`**:
  * **Qué hace:** Modela una variable individual.
  * **Atributos:** `nombre` (ej. `"ventas"`), `tipo` (`"POCION"`, `"NUMERO"`, `"CADENA"`, `"BOOLEANO"`), `valor` (el objeto real en memoria), `linea` y `columna` (dónde se creó en el archivo `.arc`).
* **`TablaSimbolos.__init__(self)`**:
  * Inicializa el diccionario `self._simbolos = {}` que almacena los pares `nombre: Simbolo`.
* **`definir(self, nombre, valor, ...)`**:
  * Si no le indican el tipo, llama a `determinar_tipo(valor)` y guarda el `Simbolo` en el diccionario.
* **`determinar_tipo(self, valor)`**:
  * Comprueba si el valor es instancia de `Pocion` $\rightarrow$ `"POCION"`, `bool` $\rightarrow$ `"BOOLEANO"`, `int/float` $\rightarrow$ `"NUMERO"`, `str` $\rightarrow$ `"CADENA"`.
* **`obtener(self, nombre, linea, columna)`**:
  * Busca la variable en el diccionario. Si no existe, lanza inmediatamente un `ErrorSemantico` informando la línea y columna exactas.
* **`obtener_pocion(self, nombre, linea, columna)`**:
  * Recupera la variable y además comprueba que `simbolo.tipo == "POCION"`. Si alguien intenta aplicar una operación tabular sobre un número, lanza un error de tipos.
* **`verificar_columna(self, nombre_pocion, nombre_columna, ...)`**:
  * Comprueba que `nombre_columna` esté dentro de `pocion.columnas`. Si no existe, detiene la ejecución y le muestra al usuario la lista de columnas que sí están disponibles.
* **`imprimir(self)`**:
  * Imprime en pantalla el estado final de todas las variables que quedaron en memoria al terminar la ejecución.

---

### ARCHIVO 3: `src/errores.py` (Gestión de Fallas)

* **`class ErrorSemantico(Exception)`**:
  * Excepción personalizada de Python que almacena el mensaje de error, la línea y la columna. Su método `__str__` formatea el texto en español claro: `[Error Semántico] Línea X, Columna Y: mensaje`.
* **`class ManejadorErrores(ErrorListener)`**:
  * Hereda de la clase `ErrorListener` de ANTLR. Intercepta los errores sintácticos y léxicos antes de que ANTLR tire textos feos en inglés. Traduce mensajes como `"mismatched input"` a `"Token inesperado"` e `"extraneous input"` a `"Elemento sobrante"`.

---

### ARCHIVO 4: `src/motor.py` (Fachada de Procesamiento)

* **`class MotorDatos`**:
  * Aplica el patrón de diseño **Fachada (Facade)**. Agrupa métodos estáticos (`cargar_csv`, `recolectar`, `purificar`, `ordenar`, `transmutar`, `sanar_descartar_nulos`, `destilar`, `describir`, `azar`, `muestra_aleatoria`) y redirige cada llamada al método correspondiente de `Pocion`. Permite que el Visitor no dependa directamente de los detalles internos de la clase `Pocion`.

---

### ARCHIVO 5: `src/visitor.py` (Intérprete Semántico - Patrón Visitor)
Es el motor de ejecución. Recorre cada nodo del árbol de análisis sintáctico (AST) generado por ANTLR.

* **`class RecetaAlquimica`**:
  * Guarda la definición de una función propia: su nombre, su lista de parámetros, las instrucciones (`hechizos`) que contiene y la expresión de retorno (`devolver`).
* **`ArcanumVisitorEjecutor.__init__(self, tabla_simbolos)`**:
  * Inicializa la tabla de símbolos, `self._fila_activa = None` (guarda la fila que se está evaluando en filtros o transmutaciones), `self._recetas_locales` (funciones del script actual), `self._compendios` (librerías cargadas) y `self._marcos_locales = []` (pila de llamadas para variables locales).
* **`visitPrograma` / `visitHechizo`**:
  * Recorren secuencialmente cada instrucción del script.
* **`visitAsignacion`**:
  * Evalúa la expresión a la derecha del `=` y guarda el resultado. Si estamos dentro de una receta, lo guarda en el marco local actual (`self._marcos_locales[-1]`); si estamos en el programa principal, lo guarda en la `TablaSimbolos` global.
* **`visitInvocarExpr`**:
  * Extrae la ruta entre comillas y llama a `MotorDatos.cargar_csv()`.
* **`visitRecolectarExpr`**:
  * Valida que las columnas pedidas existan con `tabla.verificar_columnas()` y llama a `MotorDatos.recolectar()`.
* **`visitPurificarExpr`**:
  * Define la función `evaluador_condicion_fila(fila)`: activa temporalmente `self._fila_activa = fila`, visita el subárbol de la condición y restaura la fila anterior. Llama a `MotorDatos.purificar()`.
* **`visitOrdenarExpr`**:
  * Valida la columna, revisa si dice `asc` o `desc`, y llama a `MotorDatos.ordenar()`.
* **`visitTransmutarExpr`**:
  * Activa la fila actual en `self._fila_activa`, evalúa la expresión aritmética para esa fila y llama a `MotorDatos.transmutar()`.
* **`visitSanarExpr`**:
  * Si la orden es `descartar_nulos`, llama a `sanar_descartar_nulos()`. Si es `llenar`, evalúa el valor de relleno y llama a `sanar_llenar_nulos()`.
* **`visitDestilarExpr`**:
  * Extrae las columnas agrupadoras y la lista de funciones agregadas (`suma`, `media`, etc.). Llama a `MotorDatos.destilar()`.
* **`visitInstruccionRevelar` y `visitInstruccionDescribir`**:
  * Obtienen la poción de la tabla de símbolos y llaman a `.mostrar()`.
* **`visitInstruccionPreservar`**:
  * Llama a `MotorDatos.guardar_csv()` para exportar los datos al archivo CSV indicado.
* **`visitInstruccionUsar`**:
  * Abre el archivo del compendio en `compendios/<nombre>.arc`, lo parsea con ANTLR en un subárbol independiente y guarda sus recetas en `self._compendios[nombre]`.
* **`visitDefinicionReceta`**:
  * Registra la función en `self._recetas_locales`.
* **`visitLlamadaReceta`**:
  * Resuelve la llamada a una función:
    1. Si es llamada calificada (`compendio.receta`), la busca en `self._compendios`.
    2. Si es llamada simple, la busca en `self._recetas_locales`, luego en compendios.
    3. Si no existe pero se llama `random`, `aleatorio` o `azar`, ejecuta la función de azar nativa del lenguaje.
    4. Crea un marco de variables locales con `dict(zip(parametros, argumentos))` y lo empuja a la pila (`self._marcos_locales.append()`).
    5. Ejecuta las instrucciones de la receta y retorna el resultado de `devolver`.
    6. Al finalizar, saca el marco de la pila con `self._marcos_locales.pop()` para aislar la memoria.
* **`visitIdentificador`**:
  * Resuelve el valor de una variable buscando en orden de alcance (scoping):
    1. En los parámetros o variables locales de la receta actual.
    2. En los nombres de columna de la fila activa (`self._fila_activa`) si estamos dentro de un filtro o transmutación.
    3. En la tabla de símbolos global.
    4. Si no la encuentra en ningún lado, lanza un `ErrorSemantico`.

---

### ARCHIVO 6: `src/main.py` (Punto de Entrada CLI)

* **`imprimir_arbol(nodo, parser, sangria=0)`**:
  * Función recursiva que recorre el árbol sintáctico generado por ANTLR e imprime los nombres de las reglas y los tokens terminales con sangrías si se pasa la bandera `--arbol`.
* **`ejecutar(ruta_archivo, mostrar_arbol=False)`**:
  * Coordina las fases del compilador:
    1. Lee el archivo fuente con `FileStream`.
    2. Ejecuta el `ArcanumLexer` para separar en tokens.
    3. Ejecuta el `ArcanumParser` para construir el árbol de sintaxis.
    4. Si hay errores léxicos o sintácticos, los imprime y se detiene.
    5. Si el análisis sintáctico es correcto, crea la `TablaSimbolos` y el `ArcanumVisitorEjecutor`.
    6. Llama a `visitor.visit(arbol)` para ejecutar el programa.
    7. Captura cualquier `ErrorSemantico` y lo muestra limpiamente en consola.
