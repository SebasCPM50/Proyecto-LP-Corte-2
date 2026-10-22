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

Aquí tienes el desglose exacto de cada archivo y de cada método con sus bloques de código reales y números de línea para que, si el profesor señala la pantalla y te pregunta *"¿Qué hace esta línea?"*, respondas con total seguridad.

---

### ARCHIVO 1: `src/pocion.py` (Estructura Tabular Artesanal)
Es el archivo más importante de todo el proyecto (444 líneas). Reemplaza a Pandas y NumPy desde cero.

#### 1. Inferencia Dinámica de Tipos de Celdas (`_convertir_tipo_dato`)
* **Ubicación:** Líneas 18 a 53 en `src/pocion.py`
```python
def _convertir_tipo_dato(texto):
    texto = texto.strip()
    if texto == "" or texto.upper() in ["NAN", "NULL", "NONE"]:
        return None
    if texto.lower() in ["verdadero", "true"]:
        return True
    if texto.lower() in ["falso", "false"]:
        return False
    try:
        return int(texto)
    except ValueError:
        pass
    try:
        return float(texto)
    except ValueError:
        pass
    if (texto.startswith('"') and texto.endswith('"')) or (texto.startswith("'") and texto.endswith("'")):
        return texto[1:-1]
    return texto
```
* **Qué hace:** Recibe el texto crudo de una celda del CSV y deduce si representa un entero, un decimal, un booleano, un valor nulo (`None`) o una cadena limpia.
* **Cómo funciona por dentro:** Aplica una heurística en cascada: limpia espacios con `.strip()`, detecta cadenas vacías o `'NaN'/'NULL'` para devolver `None` nativo, detecta booleanos, intenta parsear con `int()`, luego con `float()`, remueve comillas circundantes si existen y, si nada coincide, conserva el texto original.
* **Qué decirle al profesor:** *"Es nuestro analizador léxico de celdas. Infiere dinámicamente si el dato es entero, flotante, booleano, texto o nulo sin usar librerías externas"*.

#### 2. Generador Congruencial Lineal de Números Aleatorios (`_generar_siguiente_azar` y `numero_aleatorio`)
* **Ubicación:** Líneas 56 a 76 en `src/pocion.py`
```python
_semilla_azar = (id(object()) * 31 + os.getpid()) & 0x7fffffff

def _generar_siguiente_azar():
    global _semilla_azar
    _semilla_azar = (_semilla_azar * 1103515245 + 12345) & 0x7fffffff
    return _semilla_azar

def numero_aleatorio(minimo=0, maximo=1):
    azar_crudo = _generar_siguiente_azar() / 2147483647.0
    if minimo == 0 and maximo == 1:
        return round(azar_crudo, 4)
    if isinstance(minimo, int) and isinstance(maximo, int):
        rango = (maximo - minimo) + 1
        return minimo + int(azar_crudo * rango)
    return round(minimo + azar_crudo * (maximo - minimo), 4)
```
* **Qué hace:** Genera números pseudoaleatorios matemáticos escalares sin importar la librería `random` de Python.
* **Cómo funciona por dentro:** Implementa un Generador Congruencial Lineal (LCG) usando la relación de recurrencia $X_{n+1} = (a \cdot X_n + c) \pmod m$, con los multiplicadores clásicos de ANSI C ($a = 1103515245$, $c = 12345$, $m = 2^{31} - 1$). La semilla inicial se toma mezclando la dirección de memoria de un objeto efímero con el PID del proceso del sistema operativo.
* **Qué decirle al profesor:** *"Es el algoritmo de Lehmer / Congruencial Lineal programado a mano para generar números al azar sin usar `import random`"*.

#### 3. Estructura Interna e Inmutabilidad (`Pocion.__init__`)
* **Ubicación:** Líneas 86 a 99 en `src/pocion.py`
```python
class Pocion:
    def __init__(self, columnas, filas):
        self.columnas = [str(c).strip() for c in columnas]
        self.filas = [dict(f) for f in filas]

    def __len__(self):
        return len(self.filas)

    def __repr__(self):
        return f"<Pocion: {len(self.filas)} registros x {len(self.columnas)} ingredientes>"
```
* **Qué hace:** Constructor de la estructura en memoria de la tabla de datos.
* **Cómo funciona por dentro:** Guarda la lista de columnas en `self.columnas` y las filas como una lista de diccionarios independientes (`[dict(f) for f in filas]`). Al clonar cada diccionario, previene efectos secundarios y garantiza el principio de inmutabilidad funcional.
* **Qué decirle al profesor:** *"Elegimos una lista de diccionarios porque permite acceso por clave $\mathcal{O}(1)$ a cada columna de una fila y garantiza independencia total entre transformaciones"*.

#### 4. Lector Artesanal de Archivos CSV (`Pocion.desde_csv`)
* **Ubicación:** Líneas 119 a 164 en `src/pocion.py`
```python
@classmethod
def desde_csv(cls, ruta, linea=None, columna=None):
    ruta_resuelta = cls.resolver_ruta(ruta)
    if not os.path.exists(ruta_resuelta):
        raise ErrorSemantico(f"No se pudo invocar el archivo: no existe '{ruta}'", linea, columna)
    try:
        with open(ruta_resuelta, mode="r", encoding="utf-8") as f:
            lineas = [l.strip() for l in f.readlines() if l.strip()]
        if not lineas:
            return cls([], [])
        cabecera = [col.strip().strip('"') for col in lineas[0].split(",")]
        filas = []
        for num_linea, linea_texto in enumerate(lineas[1:], start=2):
            partes = linea_texto.split(",")
            while len(partes) < len(cabecera):
                partes.append("")
            fila_dict = {}
            for idx, nombre_col in enumerate(cabecera):
                valor_crudo = partes[idx] if idx < len(partes) else ""
                fila_dict[nombre_col] = _convertir_tipo_dato(valor_crudo)
            filas.append(fila_dict)
        return cls(cabecera, filas)
    except Exception as e:
        raise ErrorSemantico(f"Error al leer el archivo CSV '{ruta}': {str(e)}", linea, columna)
```
* **Qué hace:** Carga cualquier dataset CSV en disco sin importar el módulo `csv` ni Pandas.
* **Cómo funciona por dentro:** Abre el archivo con `open(encoding='utf-8')` y lo divide con `readlines()`. Toma la primera línea como cabecera y, para cada renglón subsiguiente, separa por comas con `split(',')`, normaliza la longitud y procesa cada campo mediante `_convertir_tipo_dato()`.
* **Para la prueba trampa del profesor:** Si el profesor modifica o borra filas en vivo del CSV, `readlines()` lee dinámicamente las filas existentes, adaptando la tabla sin depender de tamaños prefijados.

#### 5. Escritor y Exportador a CSV (`Pocion.a_csv`)
* **Ubicación:** Líneas 166 a 193 en `src/pocion.py`
```python
def a_csv(self, ruta, linea=None, columna=None):
    try:
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
        with open(ruta, mode="w", encoding="utf-8") as f:
            f.write(",".join(self.columnas) + "\n")
            for fila in self.filas:
                valores = []
                for col in self.columnas:
                    v = fila.get(col)
                    valores.append("" if v is None else str(v))
                f.write(",".join(valores) + "\n")
        return ruta
    except Exception as e:
        raise ErrorSemantico(f"No se pudo preservar la poción en '{ruta}': {str(e)}", linea, columna)
```
* **Qué hace:** Serializa la tabla y la persiste en el disco físico bajo el formato CSV.
* **Cómo funciona por dentro:** Si el directorio de destino no existe (por ejemplo `salidas/`), lo crea con `os.makedirs()`. Luego escribe la cabecera separada por comas y recorre cada fila convirtiendo los valores a cadena, guardando los nulos `None` como celdas vacías.

#### 6. Proyección de Columnas (`Pocion.recolectar`)
* **Ubicación:** Líneas 195 a 205 en `src/pocion.py`
```python
def recolectar(self, lista_columnas):
    nuevas_filas = []
    for fila in self.filas:
        nueva_fila = {c: fila.get(c) for c in lista_columnas}
        nuevas_filas.append(nueva_fila)
    return Pocion(lista_columnas, nuevas_filas)
```
* **Qué hace:** Proyección relacional ($\pi$). Descarta las columnas no deseadas.
* **Cómo funciona por dentro:** Itera sobre cada fila y genera por comprensión de diccionarios un nuevo objeto que solo contiene las claves solicitadas, retornando una `Pocion` nueva.

#### 7. Filtrado Booleano de Filas (`Pocion.purificar`)
* **Ubicación:** Líneas 207 a 213 en `src/pocion.py`
```python
def purificar(self, evaluador_condicion):
    nuevas_filas = [f.copy() for f in self.filas if evaluador_condicion(f)]
    return Pocion(self.columnas, nuevas_filas)
```
* **Qué hace:** Selección relacional ($\sigma$). Filtra registros según un predicado lógico.
* **Cómo funciona por dentro:** Recibe un callback `evaluador_condicion`. Mediante list comprehension, evalúa cada fila `f` y conserva copias únicamente de aquellas donde la condición devuelve `True`.

#### 8. Ordenamiento Seguro con Tratamiento de Nulos (`Pocion.ordenar`)
* **Ubicación:** Líneas 215 a 228 en `src/pocion.py`
```python
def ordenar(self, columna, ascendente=True):
    def clave_orden(fila):
        v = fila.get(columna)
        if v is None:
            return (1, 0)
        return (0, v)

    filas_ordenadas = sorted(self.filas, key=clave_orden, reverse=not ascendente)
    return Pocion(self.columnas, filas_ordenadas)
```
* **Qué hace:** Ordena las filas de forma ascendente o descendente sin fallar ante celdas nulas.
* **Cómo funciona por dentro:** Usa `sorted()` con una tupla clave: `(0, valor)` para datos reales y `(1, 0)` para `None`. En Python, las tuplas se comparan elemento por elemento, garantizando que el `0` siempre preceda al `1`, enviando todos los nulos al final de la tabla de forma segura sin producir errores de tipo.

#### 9. Creación de Columnas Calculadas (`Pocion.transmutar`)
* **Ubicación:** Líneas 230 a 246 en `src/pocion.py`
```python
def transmutar(self, nombre_columna, evaluador_expresion):
    nuevas_cols = list(self.columnas)
    if nombre_columna not in nuevas_cols:
        nuevas_cols.append(nombre_columna)
    nuevas_filas = []
    for fila in self.filas:
        copia = fila.copy()
        copia[nombre_columna] = evaluador_expresion(fila)
        nuevas_filas.append(copia)
    return Pocion(nuevas_cols, nuevas_filas)
```
* **Qué hace:** Aplica una fórmula matemática fila por fila y guarda el resultado en una columna nueva.
* **Cómo funciona por dentro:** Agrega el nuevo identificador a las cabeceras y para cada registro evalúa `evaluador_expresion(fila)`, asociando el resultado calculado a la nueva clave en un diccionario clonado.

#### 10. Sanación y Tratamiento de Nulos (`sanar_descartar_nulos` y `sanar_llenar_nulos`)
* **Ubicación:** Líneas 248 a 272 en `src/pocion.py`
```python
def sanar_descartar_nulos(self):
    filas_limpias = []
    for fila in self.filas:
        tiene_nulo = any(fila.get(c) is None for c in self.columnas)
        if not tiene_nulo:
            filas_limpias.append(fila.copy())
    return Pocion(self.columnas, filas_limpias)

def sanar_llenar_nulos(self, columna, valor_relleno):
    nuevas_filas = []
    for fila in self.filas:
        copia = fila.copy()
        if copia.get(columna) is None:
            copia[columna] = valor_relleno
        nuevas_filas.append(copia)
    return Pocion(self.columnas, nuevas_filas)
```
* **Qué hace:** Limpia y prepara datasets con valores incompletos.
* **Cómo funciona por dentro:** `sanar_descartar_nulos()` elimina cualquier fila donde `any(...)` detecte al menos un `None`. `sanar_llenar_nulos()` busca únicamente las celdas nulas de una columna dada e imputa el valor por defecto provisto (por ejemplo `0.0`), preservando la integridad del resto de registros.

#### 11. Agrupación y Funciones de Agregación (`Pocion.destilar`)
* **Ubicación:** Líneas 274 a 351 en `src/pocion.py`
```python
def destilar(self, columnas_grupo, lista_agregaciones):
    grupos = {}
    for fila in self.filas:
        clave = tuple(fila.get(col) for col in columnas_grupo)
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(fila)

    columnas_resumen = list(columnas_grupo)
    for ag in lista_agregaciones:
        if ag["alias"] not in columnas_resumen:
            columnas_resumen.append(ag["alias"])

    filas_resumen = []
    for clave, filas_del_grupo in grupos.items():
        fila_nueva = {col: clave[idx] for idx, col in enumerate(columnas_grupo)}
        for ag in lista_agregaciones:
            fn = ag["funcion"].lower()
            col_obj = ag.get("columna")
            alias = ag["alias"]
            valores = [f[col_obj] for f in filas_del_grupo if f.get(col_obj) is not None and isinstance(f.get(col_obj), (int, float))] if col_obj else []
            n = len(valores)
            if fn in ["contar", "conteo"]: resultado = len(filas_del_grupo)
            elif fn == "suma": resultado = sum(valores) if valores else 0
            elif fn in ["media", "promedio"]: resultado = (sum(valores) / n) if n > 0 else 0.0
            elif fn == "mediana":
                if not valores: resultado = 0.0
                else:
                    ord_v = sorted(valores)
                    mitad = n // 2
                    resultado = ord_v[mitad] if n % 2 == 1 else (ord_v[mitad-1] + ord_v[mitad]) / 2.0
            elif fn in ["minimo", "min"]: resultado = min(valores) if valores else 0
            elif fn in ["maximo", "max"]: resultado = max(valores) if valores else 0
            elif fn in ["desviacion", "std"]:
                if n <= 1: resultado = 0.0
                else:
                    prom = sum(valores) / n
                    resultado = (sum((x - prom) ** 2 for x in valores) / (n - 1)) ** 0.5
            fila_nueva[alias] = resultado
        filas_resumen.append(fila_nueva)
    return Pocion(columnas_resumen, filas_resumen)
```
* **Qué hace:** Agrupación y cálculo de agregaciones estadísticas (`GROUP BY`).
* **Cómo funciona por dentro:** Agrupa en una tabla hash `grupos{}` usando como clave una tupla con los valores de las columnas agrupadoras en tiempo $\mathcal{O}(N)$. Para cada grupo calcula: conteo, suma, media, mediana matemática (con interpolación para longitudes pares), mínimo, máximo y desviación estándar muestral con corrección de Bessel ($n - 1$).

#### 12. Muestreo Aleatorio sin Reemplazo (`Pocion.muestra_aleatoria`)
* **Ubicación:** Líneas 428 a 443 en `src/pocion.py`
```python
def muestra_aleatoria(self, cantidad):
    if cantidad >= len(self.filas):
        return Pocion(self.columnas, [f.copy() for f in self.filas])
    indices = list(range(len(self.filas)))
    for i in range(len(indices) - 1, 0, -1):
        j = _generar_siguiente_azar() % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    filas_muestra = [self.filas[idx].copy() for idx in indices[:cantidad]]
    return Pocion(self.columnas, filas_muestra)
```
* **Qué hace:** Extrae una muestra aleatoria de N filas de la tabla.
* **Cómo funciona por dentro:** Aplica el algoritmo de Fisher-Yates de barajado en tiempo $\mathcal{O}(N)$: itera de atrás hacia adelante intercambiando `indices[i]` con un índice al azar generado por nuestro LCG. Luego extrae los primeros `cantidad` elementos.

---

### ARCHIVO 2: `src/tabla_simbolos.py` (Memoria Semántica)
Administra las variables declaradas, su tipado semántico y la validación de columnas (134 líneas).

#### 1. Definición y Determinación de Tipos (`Simbolo` y `TablaSimbolos.definir`)
* **Ubicación:** Líneas 12 a 67 en `src/tabla_simbolos.py`
```python
class Simbolo:
    def __init__(self, nombre, tipo, valor, linea=None, columna=None):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

class TablaSimbolos:
    def __init__(self):
        self._simbolos = {}

    def definir(self, nombre, valor, tipo_sugerido=None, linea=None, columna=None):
        if tipo_sugerido is None:
            tipo_sugerido = self.determinar_tipo(valor)
        simbolo = Simbolo(nombre, tipo_sugerido, valor, linea, columna)
        self._simbolos[nombre] = simbolo
        return simbolo

    def determinar_tipo(self, valor):
        if isinstance(valor, Pocion): return "POCION"
        elif isinstance(valor, bool): return "BOOLEANO"
        elif isinstance(valor, (int, float)): return "NUMERO"
        elif isinstance(valor, str): return "CADENA"
        return "DESCONOCIDO"
```
* **Qué hace:** Almacena cada variable en memoria junto a sus metadatos (nombre, tipo inferido, valor real, coordenadas en el archivo fuente).
* **Cómo funciona por dentro:** Cuando una expresión se asigna, `determinar_tipo()` clasifica dinámicamente si es `POCION`, `NUMERO`, `CADENA` o `BOOLEANO`, registrándola en el diccionario interno `_simbolos`.

#### 2. Comprobaciones de Tipo y Existencia de Columnas (`obtener_pocion` y `verificar_columna`)
* **Ubicación:** Líneas 72 a 107 en `src/tabla_simbolos.py`
```python
def obtener(self, nombre, linea=None, columna=None):
    if nombre not in self._simbolos:
        raise ErrorSemantico(f"La variable o poción '{nombre}' no ha sido declarada o invocada previamente", linea, columna)
    return self._simbolos[nombre]

def obtener_pocion(self, nombre, linea=None, columna=None):
    simbolo = self.obtener(nombre, linea, columna)
    if simbolo.tipo != "POCION" or not isinstance(simbolo.valor, Pocion):
        raise ErrorSemantico(f"La variable '{nombre}' es de tipo {simbolo.tipo}, no es una POCIÓN (tabla de datos)", linea, columna)
    return simbolo.valor

def verificar_columna(self, nombre_pocion, nombre_columna, linea=None, columna=None):
    pocion = self.obtener_pocion(nombre_pocion, linea, columna)
    if nombre_columna not in pocion.columnas:
        columnas_disponibles = list(pocion.columnas)
        raise ErrorSemantico(f"La poción '{nombre_pocion}' no contiene el ingrediente (columna) '{nombre_columna}' (Disponibles: {columnas_disponibles})", linea, columna)
    return True
```
* **Qué hace:** Asegura el análisis semántico estricto antes de procesar cualquier orden.
* **Cómo funciona por dentro:** `obtener_pocion()` valida que el identificador corresponda a una tabla de datos (evita que el usuario intente ordenar o filtrar un número o cadena). `verificar_columna()` comprueba que la columna exista dentro de la cabecera antes de lanzar los algoritmos; si no existe, lista las columnas válidas disponibles.

---

### ARCHIVO 3: `src/visitor.py` (Motor de Ejecución - Patrón Visitor)
Recorre los nodos del AST generado por ANTLR y ejecuta las instrucciones del lenguaje (593 líneas).

#### 1. Control de Ámbitos y Pila de Marcos Locales (`visitAsignacion`)
* **Ubicación:** Líneas 45 a 85 en `src/visitor.py`
```python
def __init__(self, tabla_simbolos=None):
    super().__init__()
    self.tabla = tabla_simbolos if tabla_simbolos is not None else TablaSimbolos()
    self._fila_activa = None
    self._recetas_locales = {}
    self._compendios = {}
    self._marcos_locales = []

def visitAsignacion(self, ctx: ArcanumParser.AsignacionContext):
    nombre_var = ctx.ID().getText()
    linea = ctx.start.line
    columna = ctx.start.column
    valor = self.visit(ctx.expresion())
    if self._marcos_locales:
        self._marcos_locales[-1][nombre_var] = valor
    else:
        self.tabla.definir(nombre_var, valor, linea=linea, columna=columna)
    return valor
```
* **Qué hace:** Resuelve asignaciones distinguiendo variables locales de variables globales.
* **Cómo funciona por dentro:** Si `_marcos_locales` tiene marcos activos, la variable pertenece al contexto de ejecución de una receta (función) y se guarda en el tope de la pila (`[-1]`). Si la pila está vacía, se almacena en el ámbito global de `self.tabla`.

#### 2. Inyección de Contexto de Fila para Expresiones Vectorizadas (`visitPurificarExpr`)
* **Ubicación:** Líneas 116 a 137 en `src/visitor.py`
```python
def visitPurificarExpr(self, ctx: ArcanumParser.PurificarExprContext):
    nombre_pocion = ctx.ID().getText()
    linea = ctx.start.line
    columna = ctx.start.column
    pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

    def evaluador_condicion_fila(fila):
        antigua_fila = self._fila_activa
        self._fila_activa = fila
        try:
            res = self.visit(ctx.condicion())
            return bool(res)
        finally:
            self._fila_activa = antigua_fila

    resultado = MotorDatos.purificar(pocion_origen, evaluador_condicion_fila)
    descartadas = len(pocion_origen) - len(resultado)
    print(f"[Hechizo Purificación]: Poción '{nombre_pocion}' purificada ({len(resultado)} conservadas, {descartadas} descartadas)")
    return resultado
```
* **Qué hace:** Permite que las fórmulas y comparaciones de Arcanum lean directamente los nombres de las columnas.
* **Cómo funciona por dentro:** Establece `self._fila_activa = fila` temporalmente antes de visitar el subárbol sintáctico de la condición o fórmula matemática, restaurando el valor anterior en el bloque `finally`. Así, cuando el visitante encuentra un identificador (como `'unidades'`), lo busca en la fila actual.

#### 3. Carga Modular de Compendios Propios (`visitInstruccionUsar`)
* **Ubicación:** Líneas 304 a 334 en `src/visitor.py`
```python
def visitInstruccionUsar(self, ctx: ArcanumParser.InstruccionUsarContext):
    nombre_compendio = ctx.ID().getText()
    ruta_compendio = os.path.join("compendios", f"{nombre_compendio}.arc")
    if not os.path.exists(ruta_compendio):
        ruta_compendio = os.path.join(os.path.dirname(__file__), "..", "compendios", f"{nombre_compendio}.arc")
    if not os.path.exists(ruta_compendio):
        raise ErrorSemantico(f"No se encontró el compendio '{nombre_compendio}'", ctx.start.line, ctx.start.column)

    entrada = FileStream(ruta_compendio, encoding="utf-8")
    lexer = ArcanumLexer(entrada)
    tokens = CommonTokenStream(lexer)
    parser = ArcanumParser(tokens)
    arbol = parser.programa()

    sub_visitor = ArcanumVisitorEjecutor(self.tabla)
    sub_visitor.visit(arbol)
    self._compendios[nombre_compendio] = sub_visitor._recetas_locales
    print(f"[Compendio Cargado]: Librería propia '{nombre_compendio}' ({len(sub_visitor._recetas_locales)} recetas disponibles)")
    return None
```
* **Qué hace:** Permite importar bibliotecas escritas en Arcanum (como `compendios/matematicas.arc`).
* **Cómo funciona por dentro:** Lee el archivo `.arc`, invoca su propio flujo de ANTLR (Lexer -> Parser) y extrae sus recetas con un visitor auxiliar, guardándolas en el diccionario `_compendios` sin usar la instrucción `import` de Python.

#### 4. Invocación de Recetas, Manejo del Call Stack y Función Random (`visitLlamadaReceta`)
* **Ubicación:** Líneas 351 a 426 en `src/visitor.py`
```python
def visitLlamadaReceta(self, ctx: ArcanumParser.LlamadaRecetaContext):
    # 1. Soporte para la función random / aleatorio nativa
    if receta_nom.lower() in ["random", "aleatorio", "azar"]:
        from pocion import numero_aleatorio
        if len(argumentos) == 0: return numero_aleatorio()
        elif len(argumentos) == 1: return numero_aleatorio(0, argumentos[0])
        elif len(argumentos) == 2: return numero_aleatorio(argumentos[0], argumentos[1])

    # 2. Llamada a función del usuario con gestión de pila (Call Stack)
    marco_local = dict(zip(receta.parametros, argumentos))
    self._marcos_locales.append(marco_local)
    try:
        for h in receta.lista_hechizos:
            self.visit(h)
        if receta.nodo_devolver:
            return self.visit(receta.nodo_devolver.expresion())
        return None
    finally:
        self._marcos_locales.pop()
```
* **Qué hace:** Ejecuta funciones definidas por el usuario, resuelve la función `random` y gestiona el aislamiento de variables con una pila de llamadas (call stack).
* **Cómo funciona por dentro:** Empareja los parámetros con los argumentos evaluados en un diccionario `marco_local` y lo apila en `_marcos_locales`. Ejecuta los hechizos internos de la receta y, al finalizar, desapila el marco con `.pop()` en un bloque `finally`, garantizando que las llamadas recursivas tengan su propia memoria independiente.

#### 5. Precedencia en la Resolución de Identificadores (`visitIdentificador`)
* **Ubicación:** Líneas 564 a 593 en `src/visitor.py`
```python
def visitIdentificador(self, ctx: ArcanumParser.IdentificadorContext):
    nombre = ctx.getText()
    linea = ctx.start.line
    columna = ctx.start.column

    # 1. Busca en variables locales / parámetros de la receta activa
    if self._marcos_locales and nombre in self._marcos_locales[-1]:
        return self._marcos_locales[-1][nombre]

    # 2. Busca en las columnas del registro tabular en procesamiento
    if self._fila_activa is not None and nombre in self._fila_activa:
        return self._fila_activa[nombre]

    # 3. Busca en la tabla de símbolos global
    if self.tabla.existe(nombre):
        return self.tabla.obtener_valor(nombre, linea, columna)

    raise ErrorSemantico(f"El ingrediente o variable '{nombre}' no ha sido declarada", linea, columna)
```
* **Qué hace:** Resuelve el valor de cualquier nombre o variable.
* **Cómo funciona por dentro:** Implementa una jerarquía de alcance de 3 niveles: 1) Variables locales de la función en curso, 2) Columnas de la fila tabular activa, 3) Variables globales en la tabla de símbolos. Si no existe en ningún nivel, emite un `ErrorSemantico` claro.

---

### ARCHIVO 4: `src/main.py` (CLI y Orquestación del Compilador)
Punto de entrada por consola y pipeline completo de transducción (124 líneas).

#### Pipeline Completo de Ejecución (`main.py: ejecutar`)
* **Ubicación:** Líneas 44 a 106 en `src/main.py`
```python
def ejecutar(ruta_archivo, mostrar_arbol=False):
    entrada = FileStream(ruta_archivo, encoding="utf-8")

    # Paso 1: Análisis Léxico (tokens)
    lexer = ArcanumLexer(entrada)
    tokens = CommonTokenStream(lexer)

    # Paso 2: Análisis Sintáctico (construcción del árbol)
    parser = ArcanumParser(tokens)
    arbol = parser.programa()

    # Paso 3: Análisis Semántico y Ejecución
    tabla = TablaSimbolos()
    visitor = ArcanumVisitorEjecutor(tabla)
    visitor.visit(arbol)
    tabla.imprimir()
```
* **Qué hace:** Coordina el ciclo de vida del compilador de principio a fin.
* **Cómo funciona por dentro:** Transforma el archivo de texto en un flujo de tokens con `ArcanumLexer`, construye el árbol sintáctico (AST) con `ArcanumParser` y, si no hay errores gramaticales, inicializa la `TablaSimbolos` y pasa el control al `ArcanumVisitorEjecutor` para ejecutar las instrucciones y mostrar el estado final de la memoria.

---

### ARCHIVO 5: `src/errores.py` (Diagnósticos y Manejo Amigable de Errores)
Captura y traduce los errores para presentarlos en español claro (62 líneas).

#### Excepción Semántica y Traducción de Sintaxis ANTLR (`ErrorSemantico` y `ManejadorErrores`)
* **Ubicación:** Líneas 10 a 62 en `src/errores.py`
```python
class ErrorSemantico(Exception):
    def __init__(self, mensaje, linea=None, columna=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def __str__(self):
        if self.linea is not None and self.columna is not None:
            return f"[Error Semántico] Línea {self.linea}, Columna {self.columna}: {self.mensaje}"
        return f"[Error Semántico] {self.mensaje}"

class ManejadorErrores(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        mensaje_limpio = msg
        if "mismatched input" in msg:
            mensaje_limpio = f"Token inesperado cerca de {offendingSymbol.text if offendingSymbol else ''}"
        elif "no viable alternative" in msg:
            mensaje_limpio = f"Instrucción incompleta o no reconocida cerca de {offendingSymbol.text if offendingSymbol else ''}"
        texto = f"Línea {line}, Columna {column}: {mensaje_limpio} (Detalle: {msg})"
        self.errores.append(texto)
```
* **Qué hace:** Provee reportes comprensibles ante fallos en el código fuente.
* **Cómo funciona por dentro:** `ErrorSemantico` formatea errores lógicos indicando exactamente la línea y columna del problema. `ManejadorErrores` intercepta los mensajes nativos de ANTLR en inglés (como `'mismatched input'`) y los traduce a advertencias en español claro.

---

### ARCHIVO 6: `src/motor.py` (Patrón de Diseño Fachada / Facade)
Desacopla el intérprete Visitor de los detalles de implementación interna de Pocion (76 líneas).

#### Capa de Fachada Unificada (`MotorDatos`)
* **Ubicación:** Líneas 10 a 76 en `src/motor.py`
```python
class MotorDatos:
    @staticmethod
    def cargar_csv(ruta, linea=None, columna=None):
        return Pocion.desde_csv(ruta, linea, columna)

    @staticmethod
    def purificar(pocion, evaluador_condicion):
        return pocion.purificar(evaluador_condicion)

    @staticmethod
    def destilar(pocion, columnas_grupo, lista_agregaciones):
        return pocion.destilar(columnas_grupo, lista_agregaciones)
```
* **Qué hace:** Implementa el patrón GoF Facade para centralizar las llamadas analíticas.
* **Cómo funciona por dentro:** Proporciona métodos estáticos que redirigen las peticiones del Visitor a los métodos de `Pocion`. Esto permite modificar la implementación interna de los algoritmos tabulares sin alterar la gramática ni el código del Visitor.

