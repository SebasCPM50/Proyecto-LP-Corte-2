# Manual de uso y estudio de Arcanum

Guía práctica para aprender el lenguaje, ejecutar los ejemplos y explicar el proyecto en una sustentación. Edición revisada del 18 de noviembre de 2026.

Arcanum permite leer tablas, limpiarlas, hacer cálculos, generar gráficas y probar modelos sencillos de aprendizaje automático. Escribes instrucciones en un archivo .arc y Python ejecuta el intérprete. No necesitas saber todo el código interno para empezar.

## Qué quedó listo

El proyecto recibido ya tenía condicionales, bucles, arreglos, matrices y cuatro algoritmos de aprendizaje automático. Esta entrega corrige errores, completa funciones accesibles desde Arcanum, separa responsabilidades del código y añade ejemplos para aprender por etapas.

La versión revisada pasó 81 pruebas automatizadas. También se ejecutaron los 22 ejemplos: 15 válidos y 7 inválidos intencionales dieron el resultado esperado. Las instrucciones de Windows están incluidas; la ejecución de verificación se realizó en macOS.

## Diccionario inicial

| Nombre en Arcanum | Qué significa |
| --- | --- |
| Grimorio | Un programa guardado como archivo .arc |
| Hechizo | Una instrucción del programa |
| Poción | Una tabla con filas y columnas |
| Ingrediente | Una columna de una tabla |
| Receta | Una función que recibe valores y puede devolver un resultado |
| Compendio | Un archivo de recetas reutilizables |
| Forjar | Generar una gráfica |

Empieza por las páginas 2 a 6. Después estudia tablas y recetas. Deja aprendizaje automático y la explicación interna para cuando puedas ejecutar y modificar un ejemplo por tu cuenta.

## Dónde encontrar cada tema

Instalación y primeros pasos  2–6   ·   Matrices y recetas  7–8
Tablas y gráficas  9–12   ·   Aprendizaje automático  13–15
Ejercicios y archivos disponibles  16–19   ·   Referencia  20–21
Estructuras y sustentación  22–23   ·   Problemas y práctica  24


# Instalar y ejecutar por primera vez

Descomprime Arcanum_Completo.zip. Entra en la carpeta Arcanum y abre allí una terminal. Debes ver las carpetas src, examples y datos, junto a requirements.txt. No ejecutes desde dentro de src.

## macOS o Linux

```text
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py examples/ejemplo8_control_y_listas.arc
```

## Windows con PowerShell

```text
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py examples/ejemplo8_control_y_listas.arc
```

Necesitas Python 3.10 o posterior. Si no se reconoce python3 o py, instala Python y vuelve a abrir la terminal. La instalación de dependencias requiere conexión a Internet. Los comandos anteriores usan el entorno virtual directamente, por lo que no necesitas activarlo ni cambiar la política de PowerShell.

## Cómo saber que funcionó

El ejemplo imprime Hola, Arcanum, Aprobado, el acumulado 15 y los valores de la lista. Al final aparece el mensaje de éxito y la tabla de símbolos, que resume las variables guardadas. Arreglo([...]) es la forma en que el intérprete muestra una lista.

## La segunda vez

No vuelvas a crear el entorno. Abre la terminal en Arcanum y ejecuta el último comando. Si cambias de computador, crea de nuevo el entorno e instala las dependencias allí.

El ZIP incluye los archivos que ANTLR genera. Java solo hace falta si decides modificar la gramática y regenerar esos archivos. No es necesario para usar el lenguaje.


# Orientarse y preparar un programa propio

| Carpeta o archivo | Para qué sirve |
| --- | --- |
| examples/ | Programas .arc listos para ejecutar |
| datos/ y csv/ | Archivos de entrada de los ejemplos |
| salidas/ | Tablas y gráficas producidas al ejecutar |
| compendios/ | Recetas de matemáticas y estadística |
| src/ | Código Python del intérprete |
| grammar/Arcanum.g4 | Reglas de escritura del lenguaje |
| generated/ | Lexer, parser y visitor generados por ANTLR |
| tests/ | Pruebas automáticas |
| docs/ | Manual actual e informe de revisión |
| docs/historico/ | Guías anteriores conservadas como referencia |

## Crear mi primer archivo

En un editor de texto, crea examples/mi_programa.arc. Guarda como texto UTF-8, no como documento de Word. Verifica que no termine en .arc.txt. Copia este programa:

```text
nombre = "Arcanum";
precio = 20;
cantidad = 3;
mostrar "Estoy aprendiendo " + nombre;
mostrar precio * cantidad;
```

Ejecuta desde la raíz:

```text
.venv/bin/python src/main.py examples/mi_programa.arc
```

En Windows reemplaza .venv/bin/python por .\.venv\Scripts\python.exe en todos los comandos del resto del manual. La salida numérica esperada es 60. Cambia cantidad a 5 y debe salir 100.

## Dos opciones útiles

```text
.venv/bin/python src/main.py examples/valido_asignaciones.arc --arbol
.venv/bin/python src/main.py examples/mi_programa.arc --max-iteraciones 20000
```

--arbol muestra cómo ANTLR organizó las instrucciones. --max-iteraciones cambia el límite de cada bucle mientras; el valor normal es 10000. Usa Ctrl+C para detener una ejecución desde la terminal.


# Reglas básicas para escribir Arcanum

- Las instrucciones simples terminan en punto y coma. Los bloques si, mientras, para y receta usan llaves y no llevan punto y coma después de la llave final.
- Los comentarios empiezan con # y llegan hasta el fin de la línea.
- Los textos llevan comillas dobles. Puedes escribir tildes dentro del texto. Los nombres de variables usan letras sin tilde, números y guion bajo, sin comenzar por número.
- El lenguaje distingue mayúsculas y minúsculas. Escribe las palabras reservadas en minúscula. No uses nombres como y, no, suma, media o precio de venta para una variable. Usa precio_venta.
- El signo = guarda un valor. El operador == compara dos valores. Los decimales usan punto: 3.5.

```text
edad = 21;
altura = 1.75;
mensaje = "Hola";
activo = verdadero;
frio = falso;
numeros = [10, 20, 30];
negativo = -5;
mostrar numeros[0]; # Primer elemento: 10
```

| Operación | Ejemplo y resultado |
| --- | --- |
| Suma y resta | 7 + 3 da 10; 7 - 3 da 4 |
| Multiplicar y dividir | 7 * 3 da 21; 7 / 2 da 3.5 |
| Residuo | 7 % 2 da 1 |
| Potencia | 2 ^ 3 da 8; 2 ^ 3 ^ 2 da 512 |
| Texto con + | "Total: " + 20 produce Total: 20 |
| Comparación | >, <, >=, <=, ==, != se usan en condiciones |
| Lógica | y exige ambas condiciones; o acepta una; no niega |

Primero se resuelven los paréntesis y accesos por índice, luego potencias, signo negativo, multiplicación/división/residuo y suma/resta. Por eso -2^2 da -4, pero (-2)^2 da 4. En condiciones se aplica no antes que y, y antes que o. Usa paréntesis cuando quieras que la intención sea evidente.

No hay escapes dentro de las cadenas: escribe textos sencillos sin comillas dobles internas. No existe un literal nulo para escribir en el código; los nulos llegan desde celdas vacías u otros datos de entrada.


# Tomar decisiones y repetir acciones

## Si y sino

```text
nota = 85;
si (nota >= 60) {
    mostrar "Aprobado";
} sino {
    mostrar "Pendiente";
}
```

Solo se ejecuta una de las ramas. sino es opcional. También puedes escribir si (activo) cuando activo contiene verdadero o falso. Una condición numérica considera 0 falso; una colección vacía también se considera falsa.

## Mientras

```text
contador = 1;
acumulado = 0;
mientras (contador <= 5) {
    acumulado = acumulado + contador;
    contador = contador + 1;
}
mostrar acumulado; # 15
```

Mientras repite hasta que su condición deje de cumplirse. El contador debe cambiar para que el ciclo termine. Si supera el límite de iteraciones, Arcanum muestra un error para ayudar a detectar ciclos infinitos.

## Para

```text
para valor en [10, 20, 30] {
    mostrar valor;
}
para numero en rango(1, 6) {
    mostrar numero;
}
```

El primer ciclo imprime 10, 20 y 30. El segundo imprime del 1 al 5: el límite final de rango no se incluye. No hay instrucciones break ni continue. Puedes controlar la condición de mientras o devolver desde una receta para terminarla.

Los operadores y y o usan cortocircuito. Por ejemplo, si n vale 0, en n != 0 y 10 / n > 2 no se intenta dividir por cero porque la primera comparación ya es falsa.


# Listas y operaciones funcionales

Una lista guarda varios valores en orden. En Arcanum se representa con la clase Arreglo. El índice empieza en cero. El índice -1 señala el último valor; un índice decimal se rechaza.

```text
precios = [10, 20, 30];
mostrar precios[0]; # 10
mostrar precios[-1]; # 30
mostrar longitud(precios); # 3
nuevos = anexar(precios, 40);
mostrar precios; # Sigue con 3 elementos
mostrar nuevos; # Tiene 4 elementos
```

anexar devuelve una lista nueva. No existe precios[0] = 50. Si quieres transformar una colección, usa recetas o construye una nueva lista.

## Transformar filtrar y acumular

```text
receta doble(n) { devolver n * 2; }
receta es_par(n) {
    si (n % 2 == 0) { devolver verdadero; }
    devolver falso;
}
receta acumular(a, b) { devolver a + b; }
valores = [1, 2, 3, 4, 5];
mostrar mapear(valores, "doble");
mostrar filtrar(valores, "es_par");
mostrar reducir(valores, "acumular", 0);
```

mapear aplica doble a cada valor: resulta [2, 4, 6, 8, 10]. filtrar conserva los que cumplen es_par: [2, 4]. reducir empieza con 0 y acumula: resulta 15. Escribe el nombre de la receta entre comillas; también puedes indicar un nombre de compendio, como "estadistica.calcular_rango" en reducir, que recibe dos argumentos.

## Rango con paso

```text
mostrar rango(4); # [0, 1, 2, 3]
mostrar rango(2, 7, 2); # [2, 4, 6]
mostrar rango(5, -1, -2); # [5, 3, 1]
```

El paso debe ser un entero diferente de cero. Puedes ejecutar todas estas ideas en ejemplo9_estructuras_funcionales.arc.


# Matrices y datos en dos dimensiones

Una matriz es una tabla numérica organizada por filas y columnas. Sirve para representar vectores y operaciones de álgebra lineal. Todas sus filas deben tener la misma longitud.

```text
A = matriz([[1, 2], [3, 4]]);
B = matriz([[2, 0], [1, 2]]);
mostrar A[1][0];
mostrar transpuesta(A);
mostrar sumar_matrices(A, B);
mostrar multiplicar_matrices(A, B);
```

A[1][0] vale 3: segunda fila, primera columna. transpuesta intercambia filas y columnas. La suma produce [[3, 2], [4, 6]]. El producto matricial produce [[4, 4], [10, 8]]. No se usa A * B: para matrices se llama la función correspondiente.

## Cómo entender el producto

Para la primera celda del producto, toma la primera fila de A y la primera columna de B: 1×2 + 2×1 = 4. Repite con cada fila y cada columna. Las columnas de A deben coincidir con las filas de B. Para sumar o restar, ambas matrices deben tener las mismas dimensiones.

## Más operaciones

```text
mostrar restar_matrices(A, B);
mostrar escalar_matriz(A, 3);
mostrar longitud(A); # Número de filas: 2
```

## Pasar de una tabla a una matriz

```text
mediciones = tabla(["alto", "ancho"], [[2, 3], [4, 5]]);
M = a_matriz(mediciones, ["alto", "ancho"]);
mostrar M;
altos = columna(mediciones, "alto");
mostrar altos; # [2, 4]
```

a_matriz exige columnas existentes con números y sin nulos. columna devuelve una lista de los valores de una columna. Así conectas el análisis de tablas con operaciones numéricas y modelos de aprendizaje.

La clase Matriz está en src/estructuras/matriz.py. Sus datos se guardan en filas_datos, una lista de listas. No es una implementación completa de NumPy; es una estructura educativa con estas operaciones concretas.


# Recetas y compendios

Una receta evita repetir código. Los nombres entre paréntesis son parámetros. Los valores que entregas al llamarla son argumentos. devolver entrega el resultado y termina inmediatamente la receta, incluso si aparece dentro de si o mientras.

```text
receta factorial(n) {
    si (n <= 1) { devolver 1; }
    resultado = 1;
    para i en rango(2, n + 1) {
        resultado = resultado * i;
    }
    devolver resultado;
}
mostrar factorial(5); # 120
```

Este ejemplo se usa para enteros no negativos. Una receta no comprueba por sí sola el significado de cada argumento; añade validaciones si necesitas aceptar entradas arbitrarias.

## Variables locales

Una variable asignada dentro de una receta es local. No cambia la variable global con el mismo nombre. Los parámetros también son locales. Si una receta no encuentra un nombre local, puede consultar una columna activa o una variable global. Las operaciones sobre tablas y mostrar respetan el ámbito local.

## Usar librerías escritas en Arcanum

```text
usar compendio matematicas;
usar compendio estadistica;
mostrar matematicas.calcular_iva(100, 0.19); # 19
mostrar matematicas.aplicar_descuento(100, 0.10); # 90
mostrar matematicas.potencia(2, 3); # 8
mostrar estadistica.porcentaje(25, 100); # 25
```

matematicas.arc incluye calcular_iva(subtotal, tasa), aplicar_descuento(precio, tasa_descuento), potencia(base, exp), azar(semilla, inicio, fin) y random(semilla, inicio, fin). estadistica.arc incluye calcular_rango(maximo_val, minimo_val) y porcentaje(parte, total).

Para crear otro compendio, guarda solo definiciones de recetas en compendios/mi_libreria.arc. Cárgalo con usar compendio mi_libreria;. Usa el prefijo mi_libreria. para evitar confundir una receta con una función nativa del mismo nombre. El intérprete revisa la sintaxis antes de registrar las recetas.


# Cargar y construir tablas

Una Poción guarda los nombres de sus columnas y una colección de filas. Es parecida a una hoja sencilla de cálculo. Cargar no modifica el archivo original.

```text
ventas = invocar desde "csv/ventas.csv";
vuelos = invocar desde "datos/vuelos.json";
excel = invocar desde "datos/Data.xlsx";
mostrar ventas;
describir ventas;
```

## Formatos admitidos

- CSV: primera fila con nombres de columnas; valores separados por comas. Se admiten celdas entre comillas, comas internas y saltos de línea dentro de una celda.
- JSON: usa preferiblemente una lista de objetos, con un objeto por fila. También existe lectura del formato con columnas y filas o datos.
- Excel: archivos .xlsx mediante openpyxl. Se lee la hoja activa y la primera fila se toma como encabezado. .xls antiguo no está soportado. Las fórmulas se leen con su resultado almacenado; Arcanum no recalcula Excel.

Las celdas vacías y los textos NaN, null o None se convierten en nulos al leer CSV. Los números se convierten a enteros o decimales y true/false o verdadero/falso a booleanos. Una columna de texto que contiene códigos como 001 puede perder los ceros iniciales por esta conversión automática.

## Construir una tabla sin archivos

```text
ventas = tabla(["producto", "cantidad", "precio"],
    [["Libro", 2, 10], ["Lapiz", 1, 2]]);
mostrar ventas;
```

La primera lista contiene los nombres de columna como textos. Cada lista interior representa una fila, con un valor por columna. Los nombres deben ser únicos. Para usar un nombre en instrucciones como recolectar o transmutar, elige nombres sin espacios y que no sean palabras reservadas.

## Guardar resultados

```text
preservar ventas en "salidas/mi_tabla.csv";
guardar ventas en "salidas/mi_tabla.json";
```

preservar y guardar significan lo mismo. Las carpetas de destino se crean si hace falta y un archivo existente con esa ruta se reemplaza. Solo se exportan tablas a CSV o JSON; no se exporta Excel ni se guardan modelos entrenados.


# Limpiar seleccionar filtrar y calcular

El flujo típico es cargar, limpiar, seleccionar, filtrar y calcular. Cada transformación devuelve otra Poción. Puedes guardar el resultado con un nombre nuevo para comparar antes y después.

```text
ventas = invocar desde "csv/ventas.csv";
limpias = sanar ventas llenar descuento con 0;
reducidas = recolectar [ciudad, unidades, precio] de limpias;
validas = purificar reducidas donde unidades > 0 y precio > 0;
totales = transmutar validas con total = unidades * precio;
ordenadas = ordenar totales por total desc;
mostrar ordenadas;
```

| Instrucción | Qué cambia |
| --- | --- |
| sanar t llenar columna con valor | Reemplaza los nulos de una columna por el valor indicado |
| sanar t descartar_nulos | Quita filas con nulos en cualquiera de sus columnas |
| recolectar [a, b] de t | Conserva solo las columnas indicadas |
| purificar t donde condición | Conserva filas que cumplen la condición |
| transmutar t con nueva = expresión | Crea o reemplaza una columna calculada |
| ordenar t por columna asc | Ordena de menor a mayor |
| ordenar t por columna desc | Ordena de mayor a menor |

Si omites asc o desc, el orden es ascendente. Los nulos quedan al final en ambos sentidos. Dentro de un filtro o de una fórmula, precio significa el precio de la fila que se está evaluando. Si un parámetro local tiene el mismo nombre que una columna, prevalece el parámetro: usa nombres distintos para evitar confusión.

## Filtrar con varias condiciones

```text
inventario = invocar desde "datos/inventario.csv";
seleccion = purificar inventario donde
    (stock > 0 y precio < 100) o categoria == "oferta";
mostrar seleccion;
```

Aquí se conservan Cuaderno y Libro. Los textos de una comparación llevan comillas. La operación no encuentra palabras por similitud: compara el contenido exacto. Para un relleno negativo usa por ahora una transformación o datos ya preparados; sanar llenar acepta un literal positivo, un texto o un booleano.


# Agrupar y resumir datos

destilar reúne filas que comparten una o varias columnas y calcula un resumen por grupo. Por ejemplo, convierte muchas ventas en una fila por ciudad.

```text
ventas = invocar desde "csv/ventas.csv";
validas = purificar ventas donde unidades > 0 y precio > 0;
totales = transmutar validas con total = unidades * precio;
resumen = destilar totales por [ciudad] agregar
    suma(total) como ingresos,
    media(total) como promedio_venta,
    contar() como cantidad;
mostrar resumen;
preservar resumen en "salidas/resumen_manual.csv";
```

Las partes como ingresos y como cantidad asignan nombres a las columnas del resumen. Si no das un alias, se genera uno como suma_total. contar() sin alias usa cantidad. Usa alias diferentes entre sí y diferentes de las columnas de agrupación.

| Función | Resultado por grupo |
| --- | --- |
| suma(columna) | Suma de los valores numéricos |
| media(columna) o promedio(columna) | Promedio aritmético |
| mediana(columna) | Valor central después de ordenar |
| minimo(columna) o min(columna) | Menor valor |
| maximo(columna) o max(columna) | Mayor valor |
| desviacion(columna) o std(columna) | Desviación estándar muestral, con divisor n − 1 |
| contar() o conteo() | Número de filas |
| contar(columna) | Cantidad de valores no nulos en esa columna |

Las agregaciones numéricas ignoran nulos y valores no numéricos. Si no hay números, las implementaciones devuelven 0 o 0.0; no interpretes ese cero como una medición real. La desviación es 0 con una sola observación. Agrupar también admite el alias agrupar en lugar de destilar y resumir en lugar de agregar.

## Estadísticas descriptivas

```text
describir totales;
estadisticas = describir totales;
mostrar estadisticas;
```

describir muestra conteo, media, desviación, mínimo y máximo para columnas numéricas. La versión asignada permite conservar esa tabla. Algunos valores decimales pueden tener muchos dígitos por la representación numérica de Python.


# Crear gráficas

Una gráfica se guarda como archivo PNG. No se abre una ventana automáticamente. Busca el archivo en salidas y ábrelo con tu visor de imágenes.

```text
datos = tabla(["mes", "ingreso"],
    [["Enero", 10], ["Febrero", 15], ["Marzo", 12]]);
graficar barras desde datos con
    eje_x mes, eje_y ingreso,
    titulo "Ingresos por mes",
    salida "salidas/ingresos_manual.png";
```

También puedes escribir forjar artefacto barras en lugar de graficar barras. Los nombres de las columnas van sin comillas; el título y la ruta de salida van con comillas.

| Tipo | Uso y ejes |
| --- | --- |
| barras | Comparar categorías. eje_x categoría y eje_y número |
| lineas | Mostrar evolución o una función. eje_x y eje_y |
| dispersion | Comparar dos valores numéricos. eje_x y eje_y numéricos |
| histograma | Ver distribución de una columna numérica. Indica eje_x |
| caja | Ver dispersión y valores extremos. Indica eje_y |

```text
graficar lineas desde datos con eje_x mes, eje_y ingreso,
    titulo "Evolucion", guardar como "salidas/linea_manual.png";
graficar histograma desde datos con eje_x ingreso,
    salida "salidas/histograma_manual.png";
```

salida, guardar como y guardar en pueden indicar la ruta. Si no indicas salida, se usa salidas/grafica_TIPO.png. Limpia nulos antes de graficar y usa columnas existentes. Para barras por categoría, agrupa antes si tienes varias filas con el mismo nombre; así no dibujas barras superpuestas.

Las gráficas usan Matplotlib con un modo sin interfaz gráfica. El lenguaje prepara los valores; Matplotlib dibuja y exporta a 150 DPI. No debes presentar esta parte como una biblioteca de gráficos construida enteramente desde cero.


# Aprendizaje automático con regresión

Aprendizaje automático significa ajustar un modelo a ejemplos para obtener resultados sobre nuevos datos. En Arcanum son implementaciones educativas. No hay entrenamiento automático con cualquier archivo: tú debes seleccionar y preparar los números.

## Regresión lineal

Responde preguntas que esperan un número. Busca una recta de la forma resultado = pendiente × entrada + intercepto. Esta versión usa una sola variable de entrada.

```text
entradas = [1, 2, 3, 4];
resultados = [12, 14, 16, 18];
modelo = regresion(entradas, resultados);
mostrar resumen_modelo(modelo);
mostrar predecir(modelo, 5);
mostrar predecir_lote(modelo, [5, 6]);
```

El modelo aprende resultado = 2 × entrada + 10. La predicción para 5 es 20; el lote produce [20, 22]. El modelo se calcula a partir de los datos: no se escribió esa recta como regla dentro del ejemplo.

## Qué significa entrenar

En regresión, entrenar calcula la pendiente y el intercepto mediante mínimos cuadrados. Se necesitan al menos dos pares numéricos, con igual cantidad de entradas y resultados. Si todas las entradas son iguales, esta implementación usa pendiente 0 y el promedio de los resultados.

## Interpretar el resumen

resumen_modelo muestra la recta y R², una medida de ajuste sobre los mismos datos de entrenamiento. En el ejemplo R² es 1 porque los datos están exactamente en una recta. Ese valor no demuestra que el modelo vaya a acertar con datos reales desconocidos.

## Conectar con una tabla

```text
datos = tabla(["horas", "puntaje"], [[1, 12], [2, 14], [3, 16]]);
modelo = regresion(columna(datos, "horas"),
                   columna(datos, "puntaje"));
mostrar predecir(modelo, 4); # 18
```

Una práctica correcta separa algunos datos para comprobar el modelo después de entrenarlo. Arcanum no hace esa separación ni calcula automáticamente una evaluación externa. Los valores de estos ejemplos son didácticos; no representan una garantía de predicción.


# Clasificar con KNN y agrupar con K Means

## KNN aprende de ejemplos con etiqueta

KNN busca los k ejemplos más cercanos y elige la etiqueta que más se repite. Cada ejemplo es una lista de características numéricas; todos deben tener la misma longitud.

```text
puntos = [[1, 1], [2, 1], [8, 8], [9, 9]];
etiquetas = ["bajo", "bajo", "alto", "alto"];
modelo = knn(puntos, etiquetas, 3);
mostrar predecir(modelo, [1.5, 1.2]); # bajo
mostrar predecir(modelo, [8.5, 8.8]); # alto
```

k debe ser entero positivo y no puede superar el número de ejemplos. Si lo omites, vale 3. El nuevo punto debe tener el mismo número de características. Las etiquetas devueltas son textos. En un empate gana la etiqueta que aparece primero entre los vecinos ordenados por distancia.

## K Means encuentra grupos sin etiquetas previas

```text
datos = tabla(["x", "valor"],
    [[1, 1], [2, 1], [8, 8], [9, 9]]);
agrupados = kmeans(datos, ["x", "valor"], 2);
mostrar agrupados;
```

K-Means devuelve una nueva tabla con la columna cluster. Las dos primeras filas quedan juntas y las dos últimas en otro grupo. Los nombres Cluster_1 y Cluster_2 son identificadores; no significan bueno, malo, alto o bajo.

El algoritmo inicia centros, asigna cada punto al centro más cercano, recalcula el promedio de cada grupo y repite. En esta versión hay hasta 30 iteraciones por defecto y una inicialización determinista. k debe ser positivo y no superar las filas. Si los puntos son iguales, puede haber grupos sin miembros.

## Qué debes vigilar

KNN y K-Means usan distancia euclidiana. Una característica con números muy grandes puede dominar otra que usa números pequeños. Arcanum no normaliza automáticamente. Prepara escalas comparables y elimina nulos antes de entrenar. kmeans devuelve una tabla, por lo que no se le pasa a predecir como si fuera un modelo de regresión.


# Red neuronal para XOR

XOR devuelve 1 cuando sus dos entradas son distintas y 0 cuando son iguales. Una sola recta no separa esos resultados. El perceptrón multicapa, llamado MLP, combina una capa oculta con una salida para aprender este patrón.

```text
entradas = [[0, 0], [0, 1], [1, 0], [1, 1]];
etiquetas = [0, 1, 1, 0];
red = mlp(entradas, etiquetas);
mostrar predecir_lote(red, entradas);
mostrar probabilidad(red, [0, 1]);
perdidas = historial(red);
graficar lineas desde perdidas con
    eje_x epoca, eje_y perdida,
    titulo "Entrenamiento de XOR",
    salida "salidas/xor_manual.png";
```

Las clases esperadas son [0, 1, 1, 0]. probabilidad devuelve la activación de salida entre 0 y 1, redondeada a cuatro decimales. predecir la convierte a clase usando el umbral 0.5. La palabra probabilidad aquí no garantiza que la salida esté calibrada para otros problemas.

## Parámetros opcionales

```text
red = mlp(entradas, etiquetas, 2, 3500, 1.0);
```

Después de entradas y etiquetas, los argumentos son cantidad de neuronas ocultas, épocas y tasa de aprendizaje. Esos tres valores son también los predeterminados de la función del lenguaje. Una época es una pasada sobre todos los ejemplos. La semilla fija hace reproducible el ejemplo en el mismo entorno.

## Qué contiene el historial

historial(red) devuelve una tabla con epoca y perdida. La pérdida resume el error durante el entrenamiento. Se registra cada 100 iteraciones y al final, con la época real. El ejemplo usa la mitad del error cuadrático promedio por muestra. Una pérdida menor indica mejor ajuste de esos datos, no necesariamente mejor comportamiento fuera de ellos.

## Límites del modelo

Esta implementación admite una salida binaria y etiquetas 0 o 1. No es una red para texto ni un sistema como ChatGPT. No incluye guardado de modelos, separación de conjuntos, normalización o ajuste automático. Cambiar épocas o neuronas puede cambiar el resultado y no garantiza convergencia para cualquier problema.


# Los ejercicios del profesor paso a paso

Ejecuta el archivo que reúne los cinco ejercicios:

```text
.venv/bin/python src/main.py examples/ejemplo7_casos_profesor.arc
```

## Factorial

La receta multiplica desde 1 hasta n con un mientras. factorial(5) da 120 y factorial(10) da 3628800. También se imprime factorial(100), un entero muy grande. Explica que el acumulador guarda el producto parcial y el contador avanza en cada vuelta.

## Sigmoide

Se construyen puntos de x = -6 hasta x = 6 y se calcula sigmoide(x). En x = 0 el resultado es 0.5. La curva crece y se aproxima a 0 y 1 en sus extremos. Los puntos quedan en salidas/sigmoide.csv y la imagen en salidas/6_grafica_sigmoide_tendencia.png. En esta versión la gráfica usa la función real.

## Perceptrón multicapa para XOR

Se entrena con las cuatro combinaciones posibles. Se muestran las predicciones 0, 1, 1 y 0. La imagen salidas/8_perdida_xor.png permite observar cómo cambia el error, y salidas/perdida_xor.csv guarda el historial.

## Análisis exploratorio de Excel

Se lee datos/Data.xlsx, se muestran sus 5 filas y se calculan estadísticas descriptivas. La gráfica salidas/7_eda_pasajeros_excel.png compara pasajeros por aerolínea. Análisis exploratorio significa mirar qué hay, cómo se distribuye y si existen datos faltantes antes de sacar conclusiones.

## Filtro de números primos

La receta es_primo revisa posibles divisores. Luego filtrar se aplica a rango(2, 31). El resultado esperado es [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]. Así se muestra una operación funcional sobre toda una colección, además de comprobar números individuales.

Durante la sustentación abre el archivo .arc y una de las imágenes generadas. Cambia una entrada pequeña y vuelve a ejecutar. Eso demuestra mejor la implementación que leer únicamente los resultados ya guardados.


# Catálogo de los ejemplos principales

Todos estos archivos están en examples/. Para ejecutar cualquiera usa el comando base y el nombre completo de archivo. Las salidas se crean dentro de salidas/.

```text
.venv/bin/python src/main.py examples/ejemplo1_analisis_ventas.arc
```

| Archivo | Qué demuestra y qué produce |
| --- | --- |
| ejemplo1_analisis_ventas.arc | Carga ventas, rellena descuento, filtra y calcula ingresos con descuento. Exporta resumen_ventas_ciudad.csv. Miami queda con 6870.0. |
| ejemplo2_rendimiento_estudiantil.arc | Descarta nulos, exige asistencia ≥ 75, promedia parciales y agrupa por carrera. Exporta resumen_estudiantes.csv, con 3 carreras. |
| ejemplo3_calidad_aire.arc | Rellena pm10 con 50, filtra valores positivos y agrupa por estación. Exporta resumen_calidad_aire.csv, con 4 estaciones. |
| ejemplo4_compendios_recetas.arc | Usa matematicas y estadistica, recetas locales y azar. Exporta ventas_con_librerias_propias.csv. |
| ejemplo5_caso_estudio_final.arc | Integra control de flujo, matrices, regresión, KNN, K-Means y 4 gráficas. Exporta resumen_caso_estudio_final.csv y .json. |
| ejemplo6_analisis_vuelos_json.arc | Carga vuelos JSON, selecciona retrasos y agrupa por aerolínea. Exporta resumen_retrasos_aerolineas.json y 5_grafica_retraso_aerolineas.png. |
| ejemplo7_casos_profesor.arc | Factorial, sigmoide, XOR, Excel y primos. Produce las imágenes 6, 7 y 8, junto a sigmoide.csv y perdida_xor.csv. |

El ejemplo 5 exporta las imágenes 1_grafica_barras_ciudades.png, 2_grafica_lineas_ventas.png, 3_grafica_dispersion.png y 4_grafica_histograma_precios.png. Su cálculo de total no descuenta el mismo porcentaje que el ejemplo 1: no esperes ingresos idénticos entre ambos programas.

Los archivos son programas de texto completos, no comandos sueltos para pegar en una consola Python. Léelos y modifica una copia. Los comentarios con # explican las etapas y no se ejecutan.


# Ejemplos para aprender desde cero

## La ruta recomendada

```text
.venv/bin/python src/main.py examples/ejemplo8_control_y_listas.arc
.venv/bin/python src/main.py examples/ejemplo9_estructuras_funcionales.arc
.venv/bin/python src/main.py examples/ejemplo10_ml_paso_a_paso.arc
.venv/bin/python src/main.py examples/ejemplo11_tablas_y_recetas.arc
```

| Ejemplo | Qué debes observar |
| --- | --- |
| 8 Control y listas | Mensaje inicial, si/sino, acumulador 15, recorrido de una lista y rango descendente [5, 3, 1]. |
| 9 Estructuras funcionales | La lista original se conserva; dobles [2,4,6,8,10], pares [2,4], total 15 y producto matricial [[4,4],[10,8]]. |
| 10 ML paso a paso | Regresión predice 20 y 22; KNN clasifica como bajo; K-Means crea grupos; XOR devuelve [0,1,1,0]. |
| 11 Tablas y recetas | Crea datos sin CSV, transforma una tabla dentro de una receta y exporta ejemplo11_resumen.csv. Libro tiene ingreso 50. |

## Ejemplos válidos pequeños

| Archivo | Contenido |
| --- | --- |
| valido_asignaciones.arc | Números, texto, booleanos y cálculos; total_con_descuento vale 212.5. |
| valido_carga_seleccion.arc | Carga datos/clientes.csv y conserva nombre, ciudad, edad y compras. |
| valido_filtro_avanzado.arc | Usa paréntesis, y, o y no sobre datos/inventario.csv. |
| valido_completo.arc | Carga ventas, selecciona columnas, filtra y genera salidas/grafica_barras.png. |

Ejecuta un ejemplo a la vez. Antes de correrlo, predice qué debería mostrar. Luego compara con la salida. Si cambias los datos, algunos resultados numéricos también cambiarán; eso no implica que el intérprete esté fallando.


# Ejemplos de error y archivos de datos

Los archivos que empiezan por invalido_ son ejercicios para reconocer errores. Deben terminar con mensaje de error y código de salida 1. No los uses para comprobar una instalación exitosa.

| Archivo de examples/ | Motivo del error |
| --- | --- |
| invalido_lexico.arc | Texto sin cerrar las comillas |
| invalido_lexico_caracter.arc | Símbolo ~ no admitido |
| invalido_sintactico.arc | Filtro incompleto y expresión sin terminar |
| invalido_sintactico_recolectar.arc | Falta la palabra de |
| invalido_semantico_variable.arc | Usa inventario_fantasma sin definirlo |
| invalido_semantico_columna.arc | Solicita una columna inexistente |
| invalido_semantico_tipo.arc | Intenta seleccionar columnas de un número |

## Datos disponibles

| Archivo dentro de datos/ | Filas | Contenido |
| --- | --- | --- |
| ventas.csv | 15 | Ciudad, categoría, unidades, precios y descuento |
| estudiantes.csv | 15 | Carrera, asistencia, parciales y horas de estudio |
| calidad_aire.csv | 15 | Estación, partículas, temperatura y humedad |
| vuelos.csv y vuelos.json | 15 cada uno | Aerolínea, ruta, pasajeros, boleto, retraso y distancia |
| Data.xlsx | 5 | Vuelo, aerolínea, destino, pasajeros, precio y retraso |
| clientes.csv | 3 | Nombre, ciudad, edad y compras |
| inventario.csv | 4 | Producto, stock, precio y categoría |

csv/ conserva las copias de ventas, estudiantes, calidad_aire y vuelos que usan algunos programas originales. Usa la ruta indicada en cada ejemplo. No confundas precio_boleto de vuelos.csv con precio de Data.xlsx. Estos archivos son material de demostración; no hay evidencia de procedencia operativa real en la entrega.

## Comprobar todos los ejemplos

```text
.venv/bin/python -m pytest -q
.venv/bin/python scripts/verificar_ejemplos.py
```

El segundo comando ejecuta los 22 archivos y comprueba que los inválidos fallen. También vuelve a generar salidas. El primer comando comprueba resultados y errores concretos mediante 81 pruebas.


# Referencia rápida de funciones nativas

Las funciones se usan dentro de una expresión: resultado = funcion(argumentos); o mostrar funcion(argumentos);. Los argumentos se separan con comas. Los corchetes en las firmas de esta tabla indican argumentos opcionales; no se escriben esos corchetes al llamar.

| Firma o nombre | Qué devuelve |
| --- | --- |
| longitud(coleccion) · alias len | Cantidad de elementos; en una tabla cuenta filas |
| rango(fin) o rango(inicio, fin[, paso]) | Arreglo de enteros; fin no se incluye. Alias range |
| arreglo([elementos]) | Arreglo nuevo; sin argumento queda vacío |
| anexar(arreglo, valor) | Arreglo nuevo con el valor al final |
| mapear(arreglo, "receta") | Un resultado por elemento |
| filtrar(arreglo, "receta") | Elementos cuyo predicado es verdadero |
| reducir(arreglo, "receta", inicial) | Valor acumulado; receta recibe dos argumentos |
| matriz(filas) | Matriz numérica rectangular |
| transpuesta(matriz) · transponer | Matriz con filas y columnas intercambiadas |
| sumar_matrices(A, B) | Suma de matrices de igual tamaño |
| restar_matrices(A, B) | Resta de matrices de igual tamaño |
| multiplicar_matrices(A, B) | Producto matricial |
| escalar_matriz(A, numero) | Cada celda multiplicada por el número |
| tabla(columnas, filas) | Poción construida con listas |
| columna(tabla, "nombre") | Arreglo con los valores de una columna |
| a_matriz(tabla, columnas) | Matriz con columnas numéricas seleccionadas |
| azar([minimo, maximo]) | Número pseudoaleatorio; alias random y aleatorio |
| sigmoide(numero) · sigmoid | Activación entre 0 y 1; acota la entrada a ±15 |

azar() da un decimal entre 0 y 1; azar(10) usa límites 0 y 10; azar(2, 10) usa esos límites. Con dos límites enteros distintos del caso 0 y 1 devuelve un entero, incluyendo los extremos. No es un generador para seguridad ni criptografía. Las recetas matematicas.azar y matematicas.random reciben además una semilla explícita.


# Referencia de modelos y mapa del código

| Función | Argumentos y resultado |
| --- | --- |
| regresion(x, valores) | Dos listas numéricas; devuelve un modelo. Alias regresion_lineal |
| knn(puntos, etiquetas[, k]) | Clasificador; k predeterminado 3. Alias clasificador_knn |
| kmeans(tabla, columnas[, k]) | Tabla con cluster; k predeterminado 2. Alias agrupar_kmeans |
| mlp(x, etiquetas[, ocultas, epocas, tasa]) | Red binaria; valores 2, 3500 y 1.0. Alias perceptron |
| predecir(modelo, entrada) | Predicción individual de regresión, KNN o MLP |
| predecir_lote(modelo, entradas) | Arreglo con una predicción por entrada |
| probabilidad(red, entrada) | Salida continua del MLP |
| historial(red) | Poción con épocas y pérdida del MLP |
| resumen_modelo(modelo) | Texto con recta y R² de una regresión |

## De un archivo al resultado

Archivo .arc → lexer → tokens → parser → árbol de análisis sintáctico → visitor → módulos de ejecución y datos → salida. El lexer reconoce las piezas; el parser revisa que estén bien organizadas; el intérprete comprueba tipos y ejecuta.

| Ubicación | Responsabilidad |
| --- | --- |
| src/main.py y analizador.py | Entrada por terminal y análisis validado |
| src/visitor.py | Conectar instrucciones tabulares con el motor |
| src/runtime/control.py y expresiones.py | Decisiones, bucles, operadores y acceso por índice |
| src/runtime/recetas.py y ambitos.py | Funciones, devoluciones y memoria local |
| src/runtime/nativas.py | Registrar y validar funciones del lenguaje |
| src/pocion.py y datos_io.py | Transformaciones tabulares y formatos de archivo |
| src/motor.py | Punto de acceso a operaciones de datos, ML y gráficas |
| src/estructuras/ y src/ml/ | Colecciones, matrices y algoritmos de aprendizaje |
| src/visualizacion/graficador.py | Gráficas PNG con Matplotlib |


# Estructuras de datos para la sustentación

Una estructura de datos es una manera de organizar información para que las operaciones necesarias sean claras y eficientes. En este proyecto se usan principalmente listas, diccionarios, tuplas y una pila.

| Estructura | Uso concreto y costo orientativo |
| --- | --- |
| Lista de diccionarios | Pocion.filas guarda una lista como [{"precio": 10}, {"precio": 20}]. Acceder a una fila por posición es O(1); consultar una clave tiene costo promedio O(1). |
| Lista de nombres | Pocion.columnas conserva el orden de las columnas. Buscar si un nombre está en esa lista cuesta O(c), con c columnas. |
| Lista dentro de Arreglo | Arreglo._datos conserva el orden. Indexar cuesta O(1). mapear, filtrar y reducir recorren n elementos: O(n), sin contar el costo de la receta. |
| Lista de listas | Matriz.filas_datos representa m×n valores. Suma y transpuesta cuestan O(mn). Multiplicar una matriz m×k por otra k×n cuesta O(mkn). |
| Diccionario de símbolos | TablaSimbolos._simbolos relaciona nombre con Simbolo, tipo y valor. Búsqueda promedio O(1). |
| Pila de marcos locales | _marcos_locales añade un diccionario al entrar a una receta y lo retira al salir. Así separa los parámetros y las variables de cada llamada. |
| Diccionario con claves tupla | destilar usa una tupla de valores como clave del grupo. Formar grupos cuesta O(n g) con n filas y g columnas de agrupación; para g fijo, O(n). |
| Listas de pesos | El MLP guarda matrices w1, w2 y listas b1, b2. Entrenar actualiza esos números siguiendo el error. |

O(n) significa que el trabajo crece aproximadamente con la cantidad de elementos. O(1) significa costo constante respecto a ese tamaño; en diccionarios hablamos de promedio. Ordenar filas cuesta O(n log n). Calcular una mediana dentro de un grupo requiere ordenar sus valores.

Las transformaciones devuelven nuevas colecciones y hacen copias superficiales. Esto ayuda a conservar las tablas originales durante el flujo normal del lenguaje, pero los objetos internos de Python no son profundamente inmutables.


# Cómo explicar y demostrar el proyecto

## Explicación breve

Arcanum es un lenguaje de dominio específico para trabajar con tablas y explorar aprendizaje automático. Sus instrucciones se escriben en español con una metáfora de alquimia. ANTLR reconoce la sintaxis y un intérprete en Python ejecuta las operaciones. Hay recetas, control de flujo, estructuras propias, cuatro algoritmos de ML y generación de gráficas.

## Demostración sugerida de diez minutos

- Minutos 1 y 2: ejecuta ejemplo8_control_y_listas.arc. Explica una variable, un si y el acumulador del mientras.
- Minutos 3 y 4: ejecuta ejemplo9_estructuras_funcionales.arc. Muestra que mapear produce otra lista y explica una celda del producto matricial.
- Minutos 5 y 6: ejecuta ejemplo11_tablas_y_recetas.arc. Explica la diferencia entre seleccionar columnas y filtrar filas.
- Minutos 7 y 8: ejecuta ejemplo10_ml_paso_a_paso.arc. Cambia la entrada de regresión y compara la predicción con la recta aprendida.
- Minutos 9 y 10: abre las gráficas del ejemplo7, muestra el mapa de módulos y ejecuta las pruebas.

## Preguntas frecuentes

¿Es un compilador? Tiene análisis léxico y sintáctico, pero esta versión interpreta el árbol directamente; no genera código máquina. No hay una fase separada que construya un AST propio.

¿Es funcional? Tiene operaciones que devuelven nuevas colecciones, como mapear y filtrar. También tiene reasignaciones, ciclos y entrada/salida. Por eso combina estilos declarativo, funcional e imperativo; no es puramente funcional.

¿Usa librerías? Sí: ANTLR para análisis, Matplotlib para gráficas, openpyxl para Excel y pytest para pruebas. El motor tabular, matrices y algoritmos de ML están escritos con Python sin importar pandas, NumPy o scikit-learn. Matplotlib instala NumPy indirectamente.

¿Qué cambió respecto a lo recibido? Se mantuvieron las capacidades existentes, se corrigieron errores de ámbitos, CSV, modelos y ejemplos, y se separaron nuevas responsabilidades en runtime y datos_io. El informe REVISION_Y_CAMBIOS.md detalla cada punto.

¿Qué falta para un sistema de uso real? Más evaluación de modelos, normalización, persistencia de modelos, tratamiento de entradas complejas y más funciones del lenguaje. Expón los límites con precisión; no presentes los ejemplos como evidencia de precisión general.


# Resolver problemas y practicar

| Situación | Qué hacer |
| --- | --- |
| No se reconoce python3 o py | Instala Python y abre otra terminal; comprueba --version. |
| No module named antlr4 o matplotlib | Instala requirements.txt usando el mismo Python del entorno que ejecuta el programa. |
| No encuentra el archivo de datos | Ubícate en la carpeta raíz Arcanum y revisa la ruta entre comillas. |
| Error léxico | Revisa símbolos extraños y comillas dobles sin cerrar. |
| Error sintáctico | Busca punto y coma, llaves, paréntesis o palabras como de y donde. |
| Variable no declarada | Asígnale un valor antes de usarla y comprueba mayúsculas. |
| Columna inexistente | Muestra la tabla y copia exactamente su nombre de columna. |
| Índice fuera de rango | Una lista de 3 valores usa posiciones 0, 1 y 2. |
| Límite de iteraciones | Comprueba que el contador cambia y que la condición pueda volverse falsa. |
| Error al entrenar | Revisa dimensiones, cantidad de etiquetas, nulos y parámetros positivos. |
| No aparece una ventana de gráfica | Abre el PNG guardado en salidas; el motor no abre ventanas. |

## Cinco ejercicios con respuesta

- En el mientras de la página 5, cambia contador <= 5 por contador <= 10. El acumulado debe ser 55.
- Define receta triple(n) { devolver n * 3; } y úsala con mapear([1, 2, 3], "triple"). Debe resultar [3, 6, 9].
- En el modelo de la página 13, predice la entrada 8. El resultado debe ser 26.
- Filtra datos/inventario.csv con stock == 0. Deben quedar Libro y Lapiz.
- Cambia la cantidad del Libro de 2 a 4 en la tabla de la página 9. Al calcular cantidad * precio, su total debe ser 40.

Aprende en este orden: ejecutar sin cambios, leer la salida, modificar una entrada, escribir un ejemplo propio y explicar por qué funciona. Si puedes anticipar el resultado antes de correrlo, ya estás comprendiendo el lenguaje.
