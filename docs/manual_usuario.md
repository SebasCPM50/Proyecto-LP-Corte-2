# Guía breve de Arcanum

Lo esencial para ejecutar el proyecto, entender sus instrucciones y preparar una exposición. Lee las cuatro páginas en orden y practica los ejemplos en tu computador.

## Qué es y para qué sirve

Arcanum es un lenguaje especializado para trabajar con tablas. Permite cargar datos, filtrarlos, hacer cálculos, resumirlos y crear gráficas. Se escribe con palabras en español y nombres de alquimia: una Poción es una tabla, un ingrediente es una columna y una receta es una función.

## Abrir el ZIP y ejecutar

1. Descomprime Arcanum_Completo.zip. Abre una terminal dentro de la carpeta Arcanum: allí deben verse src, examples y requirements.txt. Necesitas Python 3.10 o posterior y conexión a Internet para instalar las dependencias.

2. Ejecuta estos comandos según tu sistema. Los dos primeros preparan el entorno una sola vez; el tercero ejecuta un ejemplo.

## macOS o Linux

```text
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py examples/ejemplo8_control_y_listas.arc
```

## Windows con PowerShell

```text
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py examples/ejemplo8_control_y_listas.arc
```

3. Deben aparecer Hola, Arcanum, Aprobado y el acumulado 15, entre otros resultados. Al final se muestra la tabla de símbolos con las variables guardadas. Para correr otro ejemplo, cambia únicamente el archivo después de src/main.py.

## Dónde está cada cosa

examples contiene programas de texto con extensión .arc; datos y csv contienen tablas de entrada; salidas guarda resultados y gráficas; src contiene el intérprete en Python; docs contiene esta guía. No necesitas Java para ejecutar el ZIP.

La próxima vez solo necesitas el tercer comando. Ejecuta siempre desde la carpeta Arcanum, no desde src.


# Escribir lo básico del lenguaje

Crea examples/mi_programa.arc con un editor de texto, no con Word. Copia uno de los bloques de esta página y ejecútalo cambiando el nombre de archivo en el comando de la página 1.

## Variables y operaciones

```text
precio = 25;
cantidad = 10;
total = precio * cantidad;
mostrar total; # Muestra 250
```

Una variable guarda un valor con un nombre. = asigna; == compara. Las instrucciones simples terminan en ;, los textos usan comillas dobles y # inicia un comentario. Puedes usar +, -, *, / y % para el residuo de una división.

## Decisiones y repeticiones

```text
nota = 45;
si (nota >= 60) { mostrar "Aprobado"; }
sino { mostrar "Pendiente"; }

contador = 1;
acumulado = 0;
mientras (contador <= 3) {
    acumulado = acumulado + contador;
    contador = contador + 1;
}
mostrar acumulado; # 1 + 2 + 3 = 6

para valor en [10, 20, 30] { mostrar valor; }
```

si elige una rama: aquí muestra Pendiente. mientras repite mientras su condición sea verdadera; el contador aumenta para que termine. para recorre una colección: aquí muestra 10, 20 y 30. Los bloques usan llaves. y, o y no combinan condiciones.

## Listas y recetas

```text
numeros = [10, 20, 30];
mostrar numeros[0]; # Primera posición: 10
receta doble(n) { devolver n * 2; }
mostrar doble(5); # 10
```

Una lista agrupa valores en orden y empieza en la posición 0. Una receta permite reutilizar instrucciones: n es el parámetro; 5 es el argumento; devolver entrega el resultado. rango(1, 4) produce [1, 2, 3], sin incluir el límite final.


# Trabajar con tablas y practicar

Este programa crea datos, conserva las compras de al menos dos unidades, calcula sus totales, agrupa por producto y guarda un resumen. Puedes copiarlo en examples/mi_programa.arc.

```text
ventas = tabla(["producto", "cantidad", "precio"],
    [["Libro", 2, 10], ["Lapiz", 1, 2], ["Libro", 3, 10]]);
seleccion = purificar ventas donde cantidad >= 2;
calculada = transmutar seleccion con total = cantidad * precio;
resumen = destilar calculada por [producto]
    agregar suma(total) como ingreso;
mostrar resumen;
preservar resumen en "salidas/resumen.csv";
```

Resultado: una fila con producto Libro e ingreso 50, porque 2 × 10 + 3 × 10 = 50. La fila de Lapiz se excluye por tener cantidad 1. El archivo resumen.csv se crea en salidas.

## Palabras que necesitas recordar

| Instrucción | Qué hace |
| --- | --- |
| invocar desde "csv/ventas.csv" | Carga un archivo como tabla; se asigna a una variable. |
| recolectar [producto, precio] de ventas | Selecciona columnas. |
| purificar ventas donde cantidad >= 2 | Filtra filas según una condición. |
| transmutar ventas con total = cantidad * precio | Calcula una columna. |
| destilar … por […] agregar … | Agrupa filas y calcula sumas, medias o conteos. |
| sanar ventas llenar precio con 0 | Reemplaza valores vacíos de esa columna. |
| preservar resumen en "salidas/resumen.csv" | Guarda una tabla en CSV; también admite JSON. |

Para leer datos de un archivo, cambia la creación de la tabla por ventas = invocar desde "csv/ventas.csv"; y adapta los nombres de columna. También se pueden leer JSON y Excel .xlsx.

## Ejemplos incluidos para estudiar

Ejecuta estos archivos de examples en este orden usando el comando de la página 1:

| Archivo | Qué debes entender |
| --- | --- |
| valido_asignaciones.arc | Precio, cantidad y descuento; el total queda en 212.5. |
| ejemplo8_control_y_listas.arc | si, mientras, para y acceso a listas. |
| ejemplo11_tablas_y_recetas.arc | El flujo de tablas de arriba, organizado en una receta. |
| ejemplo7_casos_profesor.arc | Factorial, primos y una gráfica de datos Excel. |

Las gráficas se guardan como PNG en salidas; ábrelas allí. Los ejemplos que empiezan por invalido_ contienen errores intencionales: no los uses como primera demostración.


# Entender el código y explicarlo

## El recorrido de una instrucción

Ejemplo: total = 2 + 3;. El programa pasa por estas etapas:

- Lexer: lee el texto y reconoce sus piezas, llamadas tokens: el nombre total, los signos, los números y el punto y coma.
- Parser: comprueba que los tokens respeten las reglas y construye el árbol de análisis sintáctico. Todavía no calcula la suma.
- Visitor: recorre ese árbol y ejecuta las instrucciones. En este caso calcula 5 y lo asigna a total, apoyándose en los módulos necesarios.
- Tabla de símbolos: guarda el nombre, tipo y valor de las variables. Así puede recuperar total cuando otra instrucción lo necesita.

## Las estructuras de datos

Una Poción guarda sus filas en una lista de diccionarios. Cada diccionario es una fila: {"producto": "Libro", "precio": 10}. La ventaja es consultar el precio por el nombre de la columna. Un Arreglo guarda una lista ordenada; una Matriz organiza números en filas y columnas. La tabla de símbolos también usa un diccionario, pero guarda variables del programa.

## Por qué el código está dividido

visitor.py conecta las instrucciones con su ejecución. runtime separa bucles, expresiones, recetas y variables locales. pocion.py transforma tablas; datos_io.py lee y guarda archivos. estructuras contiene arreglos y matrices; visualizacion genera las gráficas. Esta separación permite cambiar una parte sin concentrar todo en un solo archivo.

## Una explicación que puedes decir en voz alta

“Arcanum es un lenguaje para cargar y analizar tablas mediante instrucciones en español. Tiene variables, condiciones, bucles y recetas. ANTLR ayuda a reconocer la sintaxis; el intérprete está hecho en Python. El parser construye un árbol y el visitor lo recorre para ejecutar. Separamos las tareas en módulos para que el código sea más fácil de mantener.”

## Si aparece un problema

- No se encuentra un archivo: abre la terminal en Arcanum y revisa la ruta escrita entre comillas.
- No module named: repite la instalación de requirements.txt con el Python del entorno virtual.
- Error léxico o sintáctico: revisa comillas, punto y coma, paréntesis y llaves.
- Variable o columna inexistente: revisa el nombre exacto y que exista antes de usarlo.

Para repasar: ejecuta el ejemplo 8, cambia la nota y el límite del bucle, y explica por qué cambia el resultado. Después ejecuta el ejemplo 11 y sigue una fila desde la entrada hasta el resumen.
