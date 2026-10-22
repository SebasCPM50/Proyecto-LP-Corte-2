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
