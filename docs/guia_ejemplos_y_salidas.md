# GUÍA PARA ENTENDER QUÉ ES CADA COSA EN LA PANTALLA, LOS EJEMPLOS Y LAS SALIDAS
# PROYECTO ARCANUM — CIENCIA DE DATOS ARTESANAL
# ASIGNATURA: LENGUAJES DE PROGRAMACIÓN Y TRANSDUCCIÓN
# DOCENTE: JOAQUÍN F. SÁNCHEZ

No te preocupes: esa pantalla que ves en la imagen no es nada raro ni misterioso. Es simplemente el intérprete de Arcanum ejecutando paso a paso una receta analítica completa y mostrando qué va pasando con los datos.

En esta guía te explico con palabras sencillas:
1. Qué significa exactamente cada cosa que se ve en la imagen que subiste
2. Qué hace cada uno de los 4 ejemplos reales del proyecto
3. Qué datos entran en los CSV y qué significan las tablas de salida
4. Cómo funciona la arquitectura interna de los códigos para que tengas todo el mapa mental claro

---

## 1. EXPLICACIÓN PASO A PASO DE LA IMAGEN QUE SUBISTE

La imagen corresponde a la ejecución de `examples/ejemplo1_analisis_ventas.arc`.  
Se divide en tres partes claramente identificables:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. TABLA SUPERIOR: Datos Crudos originales (15 filas)       │
├─────────────────────────────────────────────────────────────┤
│ 2. MENSAJES DEL MEDIO: La tubería (Pipeline) de hechizos    │
├─────────────────────────────────────────────────────────────┤
│ 3. TABLA INFERIOR: El resumen analítico final (4 filas)     │
└─────────────────────────────────────────────────────────────┘
```

---

### PARTE 1: La Tabla Superior (`ventas_crudas`)

```text
[REVELACIÓN DE LA POCIÓN 'ventas_crudas']
Dimensiones: 15 registros x 7 ingredientes
Ingredientes: ['fecha', 'ciudad', 'categoria', 'unidades', 'precio_unitario', 'precio', 'descuento']
```

#### ¿Qué es esto?
Es la instrucción `revelar ventas_crudas;`. Muestra exactamente lo que se leyó del archivo `csv/ventas.csv` sin tocar nada todavía.
* **15 registros:** Significa que el archivo tiene 15 filas de ventas
* **7 ingredientes:** Significa que tiene 7 columnas (`fecha`, `ciudad`, `categoria`, etc.)

#### ¿Por qué hay valores raros como `None`, `0` o `-1`?
Es un dataset del mundo real con "datos sucios" diseñado a propósito para demostrar que el lenguaje sabe limpiar datos:
1. **En la columna `descuento` hay celdas que dicen `None`** (ej. fila de Medellín 2026-01-08 y Barranquilla 2026-01-14): Son ventas donde el cajero olvidó registrar si había descuento.
2. **En la columna `unidades` hay valores inválidos** (ej. Cali con `-1` unidades y Cali/Bogotá con `0` unidades): Fueron errores de digitación o devoluciones que no deben contarse como compras reales.

---

### PARTE 2: Los Mensajes entre Corchetes `[Hechizo ...]`

Estos mensajes los imprime el `visitor.py` a medida que va ejecutando cada línea del código `.arc`. Te muestran la transformación de los datos en tiempo real:

#### 1. `[Hechizo Sanación]: Nulos en 'descuento' de 'ventas_crudas' rellenados con '0.0'`
* **Línea del código:** `ventas_rellenas = sanar ventas_crudas llenar descuento con 0.0;`
* **Qué hizo:** Buscó las celdas donde el descuento era `None` y les puso `0.0`. Así no perdemos esas compras y evitamos que fallen las multiplicaciones matemáticas posteriores.

#### 2. `[Hechizo Recolección]: Se seleccionaron ['fecha', ...] de 'ventas_rellenas'`
* **Línea del código:** `ventas_reducidas = recolectar [fecha, ciudad, ...] de ventas_rellenas;`
* **Qué hizo:** Hizo una proyección, conservando solo las columnas de interés y descartando columnas innecesarias.

#### 3. `[Hechizo Purificación]: Poción 'ventas_reducidas' purificada (12 conservadas, 3 descartadas)`
* **Línea del código:** `ventas_validas = purificar ventas_reducidas donde unidades > 0 y precio > 0;`
* **¿Por qué descartó 3 filas?**
  * Descartó la fila de Cali con `-1` unidades
  * Descartó la fila de Cali con `0` unidades
  * Descartó la fila de Bogotá con `0` unidades
  * **$15 - 3 = 12$ filas válidas conservadas**. ¡Todo cuadra matemáticamente a la perfección!

#### 4. `[Hechizo Transmutación]: Nuevo ingrediente 'subtotal' añadido a 'ventas_validas'`
* **Línea del código:** `ventas_subtotal = transmutar ventas_validas con subtotal = unidades * precio;`
* **Qué hizo:** Multiplicó fila por fila cuántas unidades se vendieron por su precio para saber el subtotal antes de descuento.

#### 5. `[Hechizo Transmutación]: Nuevo ingrediente 'total' añadido a 'ventas_subtotal'`
* **Línea del código:** `ventas_totales = transmutar ventas_subtotal con total = subtotal - (subtotal * descuento);`
* **Qué hizo:** Al subtotal le restó el descuento aplicado para obtener el valor final facturado.

#### 6. `[Hechizo Ordenamiento]: Poción 'ventas_totales' ordenada por 'total' (descendente)`
* **Línea del código:** `ventas_ordenadas = ordenar ventas_totales por total desc;`
* **Qué hizo:** Puso la venta más cara de primera y la más pequeña de última.

#### 7. `[Hechizo Destilación]: Resumen generado agrupando por ['ciudad'] (4 filas resultantes)`
* **Línea del código:** `resumen_ciudades = destilar ventas_ordenadas por [ciudad] agregar suma(total)...;`
* **Qué hizo:** Tomó las 12 ventas y las agrupó en las 4 ciudades disponibles (Bogotá, Medellín, Barranquilla, Cali), calculando el total ganado en cada una.

---

### PARTE 3: La Tabla Inferior (`resumen_ciudades`)

```text
[REVELACIÓN DE LA POCIÓN 'resumen_ciudades']
Dimensiones: 4 registros x 4 ingredientes
Ingredientes: ['ciudad', 'ingreso_total', 'ticket_promedio', 'total_transacciones']

ciudad         ingreso_total   ticket_promedio   total_transacciones
Bogota         1289500.0       322375.0          4
Medellin       718300.0        179575.0          4
Barranquilla   538000.0        269000.0          2
Cali           366000.0        183000.0          2
```

#### ¿Qué significan estas columnas?
* **`ciudad`:** La categoría por la que agrupamos
* **`ingreso_total`:** La suma de todos los totales vendidos en esa ciudad
* **`ticket_promedio`:** Cuánto dinero gasta en promedio una persona en cada compra en esa ciudad (`ingreso_total / total_transacciones`)
  * Ejemplo en Bogotá: $1'289.500 / 4 = 322.375$
* **`total_transacciones`:** Cuántas compras válidas se hicieron en esa ciudad
  * $4 + 4 + 2 + 2 = 12$ transacciones en total (coincide exactamente con las 12 filas purificadas)

---

## 2. QUÉ HACE CADA UNO DE LOS 4 EJEMPLOS DEL PROYECTO

Todos los ejemplos se corren igual con el comando: `python3 src/main.py examples/<nombre_ejemplo>.arc`.

---

### EJEMPLO 1: Análisis de Ventas Comerciales
* **Archivo:** `examples/ejemplo1_analisis_ventas.arc`
* **Dataset de entrada:** `csv/ventas.csv` (15 compras)
* **Archivo de salida:** `salidas/resumen_ventas_ciudad.csv`
* **Qué resuelve en la vida real:**  
  Un gerente de ventas tiene un archivo con compras de varias sucursales. Quiere saber:
  1. Cuál ciudad es la que más ingresos genera (en este caso Bogotá con $1'289.500)
  2. Cuál es el ticket promedio por compra
  3. Descartar automáticamente compras erróneas con cantidades negativas o en cero

---

### EJEMPLO 2: Rendimiento Académico Estudiantil
* **Archivo:** `examples/ejemplo2_rendimiento_estudiantil.arc`
* **Dataset de entrada:** `csv/estudiantes.csv` (12 alumnos con notas de parcial 1, parcial 2 y porcentaje de asistencia)
* **Archivo de salida:** `salidas/resumen_estudiantes.csv`
* **Qué hace el código:**
  1. **Carga los alumnos:** Lee las notas y asistencias
  2. **Sana los datos:** Si un alumno no presentó un parcial y tiene `None`, le asigna `0.0`
  3. **Purifica por asistencia:** Solo evalúa a los alumnos regulares con asistencia $\ge 75\%$
  4. **Transmuta la nota definitiva:** Calcula la nota promedio: `nota_definitiva = (nota_parcial1 + nota_parcial2) / 2`
  5. **Ordena:** De mayor nota a menor nota
  6. **Destila por carrera:** Agrupa a los estudiantes por su programa universitario (`Ingenieria`, `Medicina`, `Derecho`) y calcula el promedio de notas de la carrera, la nota máxima, la mínima y el promedio de asistencia
* **Salida que produce:** Una tabla resumen por carrera que le dice a la universidad qué carrera tiene mejor promedio.

---

### EJEMPLO 3: Monitoreo Ambiental de Calidad del Aire
* **Archivo:** `examples/ejemplo3_calidad_aire.arc`
* **Dataset de entrada:** `csv/calidad_aire.csv` (Lecturas de sensores ambientales: estación, concentración de partículas PM2.5, PM10 y temperatura)
* **Archivo de salida:** `salidas/resumen_calidad_aire.csv`
* **Qué hace el código:**
  1. **Sana sensores con falla:** Si el sensor de PM10 falló y registró nulo, le imputa el valor estándar `50.0`
  2. **Purifica lecturas:** Descarta anomalías de sensores desconectados donde las partículas o temperaturas sean $\le 0$
  3. **Transmuta el índice de toxicidad:** Calcula la proporción de micropartículas finas: `razon_pm = (pm25 / pm10) * 100`
  4. **Ordena:** De la estación más contaminada a la más limpia
  5. **Destila por estación meteorológica:** Muestra para cada estación el promedio de contaminación PM2.5, el pico máximo registrado de polución y la temperatura promedio
* **Salida que produce:** Un reporte de calidad del aire para alertas ambientales en la ciudad.

---

### EJEMPLO 4: Demostración de Compendios y Funciones Propias
* **Archivo:** `examples/ejemplo4_compendios_recetas.arc`
* **Librería que usa:** `compendios/matematicas.arc`
* **Qué demuestra este ejemplo:**  
  Demuestra que Arcanum tiene **su propio sistema modular de librerías** sin usar el `import` de Python.
  * Carga una librería con `usar compendio matematicas;`
  * Llama a funciones de la librería: `matematicas.calcular_iva(...)` y `matematicas.aplicar_descuento(...)`
  * Crea una receta local propia en el script:
    ```arc
    receta comision_vendedor(monto, tasa) {
        comision = monto * tasa;
        devolver comision;
    }
    ```
  * Llama a la función aleatoria `random(1, 100)` para generar sorteos
  * Transmuta las ventas aplicando IVA y guarda el resultado en `salidas/ventas_con_librerias_propias.csv`

---

## 3. CÓMO FUNCIONA EL MOTOR POR DEBAJO (MAPA MENTAL RÁPIDO)

Para que entiendas qué papel juega cada archivo cuando corres un ejemplo:

```
[Archivo .arc con tu código]
             │
             ▼
      (src/main.py)  ──────► Abre el archivo y coordina todo el proceso
             │
             ├──► Lexer: Lee el texto y lo divide en palabras clave (tokens)
             ├──► Parser: Revisa que la gramática esté bien escrita (sin errores de sintaxis)
             │
             ▼
     (src/visitor.py)  ────► Es el motor ejecutor: recorre el árbol de sintaxis
             │
             ├──► Consulta y guarda variables en (src/tabla_simbolos.py)
             │
             └──► Transforma los datos llamando a (src/pocion.py)
                         │
                         ├──► Carga texto plano de csv/
                         ├──► Filtra, ordena, calcula y agrupa
                         └──► Muestra tablas en terminal y guarda en salidas/
```

### Resumen de cada archivo clave en 1 frase:
* **`src/pocion.py`**: Es nuestro Pandas artesanal hecho con listas y diccionarios nativos.
* **`src/tabla_simbolos.py`**: Es la memoria del programa; revisa que las variables y columnas existan antes de operar.
* **`src/visitor.py`**: Es el cerebro que lee las instrucciones (`purificar`, `transmutar`, etc.) y las manda a ejecutar.
* **`src/main.py`**: Es el botón de encendido que recibe el archivo por terminal y arranca el compilador.
* **`src/errores.py`**: Es el traductor que muestra errores en español amigable si algo falla.

---

## 4. QUÉ DECIRLE AL PROFESOR SI TE PREGUNTA POR LA PANTALLA

Si el profesor mira la terminal y te dice: *"Bueno, explíqueme qué fue todo lo que pasó ahí"*, le dices con tranquilidad:

> *"Profesor, lo que vemos en pantalla es el ciclo completo de análisis de datos de Arcanum sobre el caso de ventas:  
> 1. Primero cargamos los datos con `invocar desde csv/ventas.csv` y los mostramos en consola con `revelar`. Notamos que hay datos sucios: celdas con descuentos vacíos (`None`) y registros inválidos con unidades en 0 o negativas.  
> 2. Luego ejecutamos el pipeline:  
>    * Con `sanar` rellenamos los descuentos vacíos con 0.0  
>    * Con `purificar` filtramos compras reales mayores a 0 unidades; el sistema descartó 3 filas erróneas y conservó 12  
>    * Con `transmutar` calculamos las columnas de subtotal y total final con descuento  
>    * Con `ordenar` organizamos de mayor a menor ingreso  
>    * Y con `destilar` agrupamos las 12 ventas por ciudad, obteniendo el reporte consolidado final con ingreso total, ticket promedio y número de transacciones  
> 3. Finalmente, con `preservar` exportamos esa tabla limpia a un archivo CSV en disco sin usar Pandas ni librerías externas."*
