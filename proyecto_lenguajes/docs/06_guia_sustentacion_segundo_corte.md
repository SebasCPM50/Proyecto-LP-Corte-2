# Guía Definitiva para Sustentación — Segundo Corte
**Proyecto:** Arcanum (DSL de Ciencia de Datos)  
**Materia:** Lenguajes de Programación y Transducción  
**Profesor:** Joaquín F. Sánchez — Semestre 2026-2  

> **⚠️ Requisito de Oro Cumplido:** CERO LIBRERÍAS EXTERNAS (Sin Pandas, Sin NumPy).  
> Todo fue construido artesanalmente desde cero con listas y diccionarios estándar de Python, más el sistema de librerías propias del lenguaje (**Compendios** y **Recetas**).

---

## 1. La Pregunta Clave: "¿Qué librerías usaron para la ciencia de datos?"

**Respuesta exacta para decir con orgullo en la sustentación:**
> *"Profesor, **NO USAMOS NINGUNA LIBRERÍA EXTERNA**. No usamos Pandas, no usamos NumPy ni ninguna herramienta prefabricada.
> Para entender a fondo cómo funciona un compilador y la gestión de memoria:
> 1. Construimos nuestra propia estructura de datos tabular llamada **`Pocion`** (`src/pocion.py`), programada 100% desde cero usando solo listas y diccionarios nativos de Python.
> 2. Implementamos a mano la lectura de archivos CSV, la selección de columnas, el filtrado con condiciones booleanas, el ordenamiento y las fórmulas estadísticas (sumas, medias, medianas, desviaciones estándar).
> 3. Implementamos el **Patrón Visitor** y la **Tabla de Símbolos** para ejecutar cada hechizo y controlar tipos y variables.
> 4. Creamos nuestro propio sistema de módulos y librerías reutilizables dentro del DSL (**Compendios y Recetas**) en la carpeta `compendios/`, que se cargan con `usar compendio` sin depender del `import` de Python."*

---

## 2. Explicación Sencilla de Cómo Funciona la Tabla de Datos Artesanal

Si el profesor les pide abrir el código de la tabla:
- Abran [`src/pocion.py`](file:///C:/Users/sebas/.gemini/antigravity/scratch/proyecto_lenguajes-main/src/pocion.py).
- Explíquenlo así de fácil:
  > *"Profesor, una `Pocion` tiene solo dos cosas adentro:
  > - `self.columnas`: una lista de nombres de columnas como `['fecha', 'ciudad', 'precio']`.
  > - `self.filas`: una lista de diccionarios, donde cada diccionario es una fila de datos, por ejemplo `{'fecha': '2026-01-05', 'ciudad': 'Bogota', 'precio': 150000}`.
  > 
  > Cuando hacemos `purificar` (filtrar), recorremos la lista de filas con un `for` y guardamos en una lista nueva solo las filas que cumplen la condición.
  > Cuando hacemos `transmutar` (columna calculada), evaluamos la fórmula para cada fila y agregamos la nueva clave al diccionario.
  > Cuando hacemos `destilar` (agrupar), agrupamos en un diccionario usando la ciudad como clave y calculamos el promedio sumando los valores y dividiendo entre la cantidad."*

---

## 3. Demostración en Vivo Frente al Profesor

Abre PowerShell en la carpeta `proyecto_lenguajes-main` y corre estos comandos:

### Paso 1: Mostrar que las pruebas automáticas pasan al 100%
```powershell
python -m pytest -v tests
```
*Qué decir:* "Aquí corremos 24 pruebas automáticas con pytest que validan nuestra tabla artesanal, la tabla de símbolos, los errores semánticos y las librerías propias".

### Paso 2: Ejecutar los casos de estudio de datos reales
```powershell
# 1. Ventas comerciales y exportación CSV
python src/main.py examples/ejemplo1_analisis_ventas.arc

# 2. Rendimiento estudiantil
python src/main.py examples/ejemplo2_rendimiento_estudiantil.arc

# 3. Monitoreo ambiental de aire
python src/main.py examples/ejemplo3_calidad_aire.arc
```
*Qué señalar:* "Fíjese en cómo el programa imprime las tablas con bordes limpios en consola usando nuestro formateador propio, genera estadísticas descriptivas y exporta los archivos CSV a la carpeta `salidas/` sin haber importado pandas".

### Paso 3: Demostrar las librerías propias del lenguaje (Compendios y Recetas)
```powershell
python src/main.py examples/ejemplo4_compendios_recetas.arc
```
*Qué señalar:* "En este cuarto ejemplo demostramos cómo Arcanum carga la librería `compendios/matematicas.arc` mediante la instrucción `usar compendio matematicas;` y llama a funciones como `matematicas.calcular_iva()`, funcionando de manera totalmente autónoma a Python".

### Paso 4: Demostrar la captura de errores semánticos
```powershell
# Probar variable no declarada
python src/main.py examples/invalido_semantico_variable.arc

# Probar columna que no existe
python src/main.py examples/invalido_semantico_columna.arc

# Probar tipo incompatible
python src/main.py examples/invalido_semantico_tipo.arc
```
*Qué señalar:* "El compilador detecta inmediatamente los errores semánticos con línea y columna y nos dice qué columnas están disponibles".

---

## 4. Preguntas Frecuentes y Respuestas Listas para Memorizar

**P1: ¿Por qué decidieron no usar Pandas ni librerías existentes?**
> *R: Porque en una clase de Lenguajes de Programación y Compiladores, usar Pandas oculta la lógica real. Al crear nuestra propia estructura de datos con listas y diccionarios, demostramos que entendemos la representación en memoria, el recorrido secuencial, el tipado y la manipulación de datos desde los fundamentos.*

**P2: ¿Cómo funciona el sistema de compendios (librerías propias)?**
> *R: Al encontrar `usar compendio matematicas;`, el intérprete busca el archivo `compendios/matematicas.arc`, lo parsea con las mismas reglas de ANTLR y guarda las funciones (`receta`) en una tabla de compendios. Cuando el código invoca `matematicas.calcular_iva()`, el Visitor busca la receta y la ejecuta creando un marco local de variables para sus argumentos.*

**P3: ¿Qué patrones de diseño aplicaron?**
> *R: Aplicamos tres patrones fundamentales:
> 1. **Patrón Visitor**: Para recorrer los nodos del árbol sintáctico generado por ANTLR y ejecutar las instrucciones.
> 2. **Patrón Tabla de Símbolos**: Para gestionar las variables y sus tipos en memoria.
> 3. **Patrón Fachada**: La clase `MotorDatos` que simplifica el acceso a las operaciones de la tabla `Pocion`.*
