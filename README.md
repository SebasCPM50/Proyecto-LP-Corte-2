# PROYECTO ARCANUM — DOCUMENTO OFICIAL DE ENTREGA Y SUSTENTACIÓN
# DSL DE CIENCIA DE DATOS CON TEMÁTICA ALQUÍMICA
# ASIGNATURA: LENGUAJES DE PROGRAMACIÓN Y TRANSDUCCIÓN
# DOCENTE: JOAQUÍN F. SÁNCHEZ
# UNIVERSIDAD SERGIO ARBOLEDA

### INFORMACIÓN DEL PROYECTO
* **Nombre del Lenguaje**: Arcanum
* **Paradigma**: Declarativo, funcional y analítico (orientado a procesamiento de datos)
* **Entregas integradas**: Entrega 1 (Gramática y Diseño) + Entrega 2 (Semántica, Motor Artesanal, Intérprete y Compendios)
* **Condición estricta**: Cero librerías externas (sin Pandas, sin NumPy, sin módulo csv de Python)

---

## RESUMEN DEL ALCANCE Y CONCEPTO

Arcanum es un lenguaje de dominio específico (DSL) diseñado para analistas y científicos de datos que buscan realizar preparación, limpieza, filtrado, transformación y agregación estadística sobre conjuntos de datos tabulares.

El lenguaje adopta una metáfora alquímica coherente donde:
* Un conjunto de datos (DataFrame) es una **Poción**
* Una columna o campo es un **Ingrediente**
* Un archivo de código o script es un **Grimorio**
* Una función reutilizable es una **Receta**
* Una librería de funciones propias es un **Compendio**

### Mapeo de Operaciones de Ciencia de Datos

| Operación estándar de datos | Término en Arcanum | Propósito analítico |
| :--- | :--- | :--- |
| `read_csv` | `invocar desde "ruta.csv"` | Carga un archivo CSV desde disco a memoria |
| `select` | `recolectar [col1, col2] de tabla` | Proyección: conserva únicamente las columnas pedidas |
| `filter` / `where` | `purificar tabla donde (condicion)` | Filtrado: conserva las filas que cumplen el predicado booleano |
| `sort_values` | `ordenar tabla por col [asc/desc]` | Ordenamiento de registros por una columna |
| `mutate` / calcular | `transmutar tabla con nuevo = formula` | Crea una columna calculada fila por fila |
| `dropna` | `sanar tabla descartar_nulos` | Limpieza: descarta filas que tengan celdas vacías |
| `fillna` | `sanar tabla llenar col con valor` | Imputación: rellena valores nulos con un valor por defecto |
| `group_by` + `aggregate` | `destilar tabla agrupar [cols] agregando [...]` | Agrupación y cálculo de métricas (suma, media, mediana, std, min, max, contar) |
| `describe` | `describir tabla` | Genera una tabla con estadísticas de columnas numéricas |
| `print` | `revelar tabla` | Muestra la tabla en consola sin recortar filas |
| `to_csv` | `preservar tabla en "ruta.csv"` | Exporta la tabla transformada a un archivo CSV en disco |
| `random` / muestreo | `random(min, max)` / `muestra_aleatoria(n)` | Generación de números aleatorios y muestreo de filas sin librerías |
| `import` propio | `usar compendio nombre` | Carga una librería propia escrita en Arcanum |
| `function` | `receta nombre(param) { ... devolver x; }` | Define y ejecuta funciones propias con memoria local |

---

## ARQUITECTURA ARTESANAL: CERO LIBRERÍAS EXTERNAS

Por requisito estricto de la asignatura, el proyecto no utiliza Pandas, NumPy ni el módulo csv estándar de Python. Todo el motor analítico fue construido desde cero utilizando únicamente los tipos de datos nativos de Python:

### Estructura de la Poción (src/pocion.py)
* `self.columnas`: Lista de nombres de columnas (`list[str]`)
* `self.filas`: Lista de diccionarios nativos (`list[dict[str, Any]]`)

```
Objeto Pocion
├── self.columnas = ['fecha', 'ciudad', 'precio']
└── self.filas = [
      {'fecha': '2026-01-05', 'ciudad': 'Bogota', 'precio': 150000},
      {'fecha': '2026-01-06', 'ciudad': 'Cali',   'precio': 95000}
    ]
```

### Principio de Inmutabilidad Alquímica
Cada operación de transformación (`recolectar`, `purificar`, `ordenar`, `transmutar`, `sanar`, `destilar`, `muestra_aleatoria`) genera y retorna una **Poción completamente nueva**, garantizando que el conjunto de datos original permanezca intacto y permitiendo encadenar análisis sin efectos secundarios no deseados.

---

## MECÁNICA DE CARGA Y LECTURA DE ARCHIVOS CSV

### Proceso en el código (`Pocion.desde_csv`)
* **Apertura del archivo físico**: Utiliza la función nativa `open(ruta, mode='r', encoding='utf-8')`
* **Lectura de líneas**: Extrae el contenido en memoria con `.readlines()` y elimina renglones vacíos
* **Extracción de cabeceras**: Toma la primera línea (`lineas[0]`), la limpia con `.strip()` y la divide por comas mediante `.split(',')`
* **Inferencia automática de tipos (`_convertir_tipo_dato`)**:
  * Si la celda está vacía o dice `"NaN"`, `"NULL"`, `"NONE"` $\rightarrow$ la convierte a `None`
  * Si dice `"verdadero"` o `"true"` $\rightarrow$ `True`
  * Si dice `"falso"` o `"false"` $\rightarrow$ `False`
  * Si contiene dígitos enteros $\rightarrow$ `int`
  * Si contiene formato decimal $\rightarrow$ `float`
  * Si es texto $\rightarrow$ elimina comillas exteriores y lo deja limpio
* **Estructuración en diccionarios**: Por cada línea crea un diccionario emparejando cada columna con su valor tipado
* **Almacenamiento**: Genera la instancia `Pocion(cabecera, filas)` y la registra en la Tabla de Símbolos

### Explicación conceptual sobre la carga de CSV
> *"Profesor, construimos nuestro propio analizador léxico de texto plano para archivos CSV sin usar Pandas ni el módulo csv de Python.  
> Abrimos el archivo físico con `open()`, extraemos los nombres de columnas de la primera línea con `.split(',')` e iteramos sobre los renglones siguientes. Implementamos una función artesanal de inferencia de tipos que convierte dinámicamente cada celda a entero, flotante, booleano, texto o nulo `None`.  
> Cada registro se representa como una tabla hash (diccionario) y la colección completa se almacena en una lista dinámica dentro de la clase Pocion, integrándose de inmediato con la Tabla de Símbolos."*

---

## ESTRUCTURAS DE DATOS UTILIZADAS

| Estructura | Dónde se utiliza | Complejidad | Justificación técnica |
| :--- | :--- | :--- | :--- |
| **Lista de Diccionarios** (`List[Dict]`) | Almacenamiento tabular en `Pocion` | Acceso a celda: $\mathcal{O}(1)$<br>Recorrido: $\mathcal{O}(N)$ | Permite consultar campos por nombre (`fila['precio']`) en lugar de índices numéricos, evitando desalineaciones al agregar o quitar columnas |
| **Tabla Hash** (`Dict[str, Simbolo]`) | Memoria en `TablaSimbolos` | Búsqueda e inserción: $\mathcal{O}(1)$ promedio | Permite verificar al instante si una variable existe y si sus tipos son compatibles |
| **Árbol n-ario jerárquico** | Árbol de Derivación (AST) de ANTLR | Recorrido: $\mathcal{O}(V)$ lineal en nodos | Modela naturalmente la precedencia de operadores matemáticos y la estructura del programa |
| **Hash Map de Agrupación** (`Dict[Tuple, List]`) | Agrupación en `Pocion.destilar` | Clasificación: $\mathcal{O}(N)$ lineal | Clasifica $N$ filas en sus categorías usando como clave una tupla de valores en una sola pasada, sin requerir ordenamiento previo ($\mathcal{O}(N \log N)$) |
| **Pila de Marcos Locales** (`Call Stack` / `List[Dict]`) | Llamadas a recetas en `visitor.py` | Push y Pop: $\mathcal{O}(1)$ | Garantiza el aislamiento de argumentos locales en recetas y permite recursión sin sobreescribir variables globales |

---

## DESGLOSE DE ARCHIVOS DEL PROYECTO

### `src/pocion.py`
Núcleo artesanal de datos. Implementa la clase `Pocion` con todos los métodos de carga, exportación, filtrado, ordenamiento, transmutación, sanación, agrupamiento, generador de números aleatorios por congruencial lineal, muestreo aleatorio de filas y visualización en consola.

### `src/tabla_simbolos.py`
Libreta de memoria del compilador. Modela cada variable mediante la clase `Simbolo` y gestiona las validaciones de tipo (`POCION`, `NUMERO`, `CADENA`, `BOOLEANO`) y existencia de columnas.

### `src/errores.py`
Manejador amigable de errores. Define la excepción `ErrorSemantico` y el `ManejadorErrores` que traduce las alertas sintácticas de ANTLR a mensajes claros en español indicando línea y columna.

### `src/motor.py`
Fachada estática que conecta las operaciones del Visitor con los métodos de la clase `Pocion`.

### `src/visitor.py`
Intérprete semántico basado en el patrón Visitor de ANTLR. Recorre el árbol sintáctico, ejecuta las transformaciones sobre las pociones, administra la pila de llamadas para recetas, resuelve llamadas nativas a funciones de azar y enlaza compendios.

### `src/main.py`
Punto de entrada de línea de comandos. Coordina el análisis léxico, el análisis sintáctico, la visualización opcional del árbol con `--arbol` y la ejecución semántica.

### `compendios/matematicas.arc` y `compendios/estadistica.arc`
Librerías propias escritas 100% en sintaxis Arcanum que proveen recetas reutilizables (`calcular_iva`, `aplicar_descuento`, `potencia`, `azar`, `random`, `calcular_rango`, `porcentaje`).

---

## CATÁLOGO DE INSTRUCCIONES Y GRAMÁTICA FORMAL (EBNF)

### Gramática EBNF Simplificada
```ebnf
programa            ::= hechizo* EOF ;
hechizo             ::= asignacion ';'
                      | instruccionUsar ';'
                      | instruccionRevelar ';'
                      | instruccionDescribir ';'
                      | instruccionPreservar ';'
                      | instruccionForjar ';'
                      | definicionReceta ;

asignacion          ::= ID '=' expresion ;

expresion           ::= invocarExpr
                      | recolectarExpr
                      | purificarExpr
                      | ordenarExpr
                      | transmutarExpr
                      | sanarExpr
                      | destilarExpr
                      | describirExpr
                      | llamadaReceta
                      | expresionAritmetica ;

invocarExpr         ::= 'invocar' 'desde' CADENA ;
recolectarExpr      ::= 'recolectar' '[' listaIds ']' 'de' ID ;
purificarExpr       ::= 'purificar' ID 'donde' '(' condicion ')' ;
ordenarExpr         ::= 'ordenar' ID 'por' ID direccionOrden? ;
transmutarExpr      ::= 'transmutar' ID 'con' ID '=' expresionAritmetica ;
sanarExpr           ::= 'sanar' ID ('descartar_nulos' | 'llenar' ID 'con' valorLiteral) ;
destilarExpr        ::= 'destilar' ID 'agrupar' '[' listaIds ']' 'agregando' '[' listaAgregaciones ']' ;

instruccionUsar     ::= 'usar' 'compendio' ID ;
definicionReceta    ::= 'receta' ID '(' listaIds? ')' '{' hechizo* instruccionDevolver? '}' ;
instruccionDevolver ::= 'devolver' expresion ';' ;
```

---

## BATERÍA COMPLETA DE PRUEBAS Y EVIDENCIAS

### Resultados del Suite Automatizado (pytest)
Se ejecutaron 28 pruebas automatizadas cubriendo todas las capas del sistema con un resultado de **100% exitoso**:

```
tests/test_unitarias.py ..............                                   [ 50%]
tests/test_semantica.py .........                                        [ 82%]
tests/test_integracion.py .....                                          [100%]

============================= 28 passed in 0.13s ==============================
```

### Pruebas Unitarias de Pocion Artesanal (`tests/test_unitarias.py`)
* `test_recolectar`: Selección de columnas y verificación de inmutabilidad
* `test_purificar`: Filtrado numérico condicional
* `test_ordenar`: Ordenamiento ascendente y descendente
* `test_transmutar`: Generación de nuevas columnas mediante fórmulas
* `test_sanar_descartar_nulos`: Eliminación de registros con celdas nulas
* `test_sanar_llenar_nulos`: Imputación de valores por defecto en nulos
* `test_destilar`: Agrupamiento multivariable con suma y conteo
* `test_muestra_aleatoria`: Extracción de subconjunto de filas al azar sin reemplazo
* `test_numero_aleatorio_artesanal`: Generación pseudoaleatoria con congruencial lineal hecho a mano sin librerías

### Pruebas Semánticas Negativas (`tests/test_semantica.py` y `examples/invalido_*.arc`)
Se verificó que el compilador capture y reporte con claridad las anomalías lógicas:

* **Variable no declarada**:
  * Archivo: `examples/invalido_semantico_variable.arc`
  * Entrada: `total = x + variable_inexistente;`
  * Salida: `[Error Semántico] Línea 3, Columna 8: La variable o ingrediente 'tasa_desconocida' no ha sido declarada o invocada previamente`
* **Columna inexistente**:
  * Archivo: `examples/invalido_semantico_columna.arc`
  * Entrada: `recolectar [columna_falsa] de datos;`
  * Salida: `[Error Semántico] Línea 4, Columna 22: La poción 'ventas' no contiene el ingrediente (columna) 'columna_inventada' (Disponibles: ['fecha', 'ciudad', 'categoria', 'unidades', 'precio_unitario'])`
* **Incompatibilidad de tipos**:
  * Archivo: `examples/invalido_semantico_tipo.arc`
  * Entrada: `recolectar [ciudad] de 0.19;`
  * Salida: `[Error Semántico] Línea 4, Columna 23: La variable 'tasa_iva' es de tipo NUMERO, no es una POCIÓN (tabla de datos)`

### Pruebas de Integración con Ejemplos Reales (`examples/`)

#### Análisis de Ventas (`examples/ejemplo1_analisis_ventas.arc`)
* Carga dataset real con 15 transacciones
* Limpia registros nulos
* Filtra ventas con unidades $\ge 2$
* Calcula columna `subtotal = unidades * precio_unitario`
* Agrupa por ciudad calculando suma de ingresos y conteo
* Exporta a `salidas/resumen_ventas_ciudad.csv`

#### Rendimiento Estudiantil (`examples/ejemplo2_rendimiento_estudiantil.arc`)
* Carga dataset de 12 estudiantes
* Imputa notas nulas asignando $0.0$
* Agrupa por carrera calculando promedio de notas
* Exporta a `salidas/resumen_estudiantes.csv`

#### Calidad del Aire (`examples/ejemplo3_calidad_aire.arc`)
* Carga mediciones de estaciones ambientales
* Descarta registros sin datos
* Filtra mediciones de temperatura $> 18$
* Agrupa por estación calculando media y desviación estándar de PM2.5
* Exporta a `salidas/resumen_calidad_aire.csv`

#### Compendios y Recetas Propias (`examples/ejemplo4_compendios_recetas.arc`)
* Importa la librería `usar compendio matematicas;`
* Invoca la receta `matematicas.calcular_iva(subtotal, 0.19)`
* Aplica descuentos calculados y muestra los resultados en la terminal

---

## GUÍA DE INSTALACIÓN Y EJECUCIÓN EN MÁQUINA VIRTUAL UBUNTU

Para ejecutar el proyecto en una máquina virtual Ubuntu Linux limpia, sigue estos pasos:

### Instalación de dependencias del sistema y entorno
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv default-jre
```

### Creación y activación del entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalación del runtime de ANTLR y pytest
```bash
pip install antlr4-python3-runtime==4.13.2 pytest
```

### Ejecución de la batería de pruebas
```bash
python3 -m pytest tests/
```

### Ejecución de los ejemplos principales
```bash
# Ejemplo 1: Ventas comerciales
python3 src/main.py examples/ejemplo1_analisis_ventas.arc

# Ejemplo 2: Rendimiento académico
python3 src/main.py examples/ejemplo2_rendimiento_estudiantil.arc

# Ejemplo 3: Calidad ambiental
python3 src/main.py examples/ejemplo3_calidad_aire.arc

# Ejemplo 4: Compendios y recetas
python3 src/main.py examples/ejemplo4_compendios_recetas.arc

# Visualizar el árbol de análisis sintáctico
python3 src/main.py examples/ejemplo1_analisis_ventas.arc --arbol
```

### Verificación de errores semánticos controlados
```bash
python3 src/main.py examples/invalido_semantico_variable.arc
python3 src/main.py examples/invalido_semantico_columna.arc
python3 src/main.py examples/invalido_semantico_tipo.arc
```
