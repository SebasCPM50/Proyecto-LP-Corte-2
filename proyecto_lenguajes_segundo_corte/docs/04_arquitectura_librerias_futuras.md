# Arquitectura de Librerías Propias ("Compendios") — Hoja de ruta Corte 2 y 3

Este documento responde al pedido explícito del profesor de mostrar,
desde el Corte 1, cómo se planea construir el sistema de librerías
propias del lenguaje Arcanum (obligatorio: no se permite usar el
mecanismo de importación de Python; el sistema de módulos debe diseñarse
desde cero como parte del propio DSL).

> **Estado actual (Corte 1):** solo se documenta y diagrama el diseño.
> Las palabras reservadas nuevas que se describen aquí (`usar`,
> `compendio`, `receta`, `devolver`) **no están implementadas todavía en
> `grammar/Arcanum.g4`**, para no ampliar el alcance mínimo de este
> corte. Se incorporarán en el Corte 3, según la tabla de fases del
> profesor.

## 1. Concepto y vocabulario nuevo

Ya que en Arcanum la palabra **grimorio** se reserva para "el programa
completo", una librería reutilizable necesita un nombre propio dentro de
la temática de alquimia: la llamaremos **compendio** (un libro de
consulta con recetas ya probadas, distinto del grimorio personal de cada
usuario).

| Concepto nuevo | Significado |
|---|---|
| **Compendio** | Un archivo `.arc` auxiliar que agrupa recetas reutilizables, en vez de ejecutarse solo |
| **Receta** | Una función reutilizable definida dentro de un compendio |
| `usar compendio nombre;` | Instrucción para importar un compendio dentro de un grimorio |
| `nombre_compendio.receta(args)` | Notación de punto para invocar una receta de un compendio |

```arc
usar compendio matematicas;

resultado = matematicas.potencia(2, 3);
```

## 2. Estructura de carpetas propuesta

```
arcanum/
└── compendios/                 # librerias propias del lenguaje (NO Python)
    ├── matematicas.arc          #   potencia, factorial, redondear...
    ├── cadenas.arc               #   mayuscula, longitud, concatenar...
    ├── estadistica.arc            #   normalizar, percentil...
    └── utilidades.arc              #   validaciones genericas
```

Cada archivo `.arc` de esta carpeta se escribe **en el propio lenguaje
Arcanum**, reutilizando el mismo Lexer/Parser del Corte 1, con la nueva
palabra reservada `receta`:

```arc
# compendios/matematicas.arc
receta potencia(base, exponente) {
    devolver base ^ exponente;
}

receta factorial(numero) {
    ...
}
```

## 3. Componentes del sistema de módulos (diseño para Corte 3)

```
┌───────────────────────────┐
│   grimorio_principal.arc   │
│   usar compendio matematicas;│
└─────────────┬───────────────┘
              │  (1) se detecta la instruccion "usar compendio"
              ▼
┌───────────────────────────────┐
│   Resolutor de Compendios       │  ← nuevo componente (Corte 3)
│   - busca compendios/<nombre>.arc │
│   - evita ciclos de importacion   │
└─────────────┬─────────────────────┘
              │ (2) reutiliza el MISMO Lexer/Parser del Corte 1
              ▼
┌───────────────────────────────┐
│  Lexer + Parser (ANTLR)         │  ← ya construido en el Corte 1
│  genera el arbol del compendio  │
└─────────────┬─────────────────────┘
              │ (3) el Visitor recorre las definiciones "receta"
              ▼
┌───────────────────────────────┐
│  Tabla de Compendios             │  ← nuevo componente (Corte 3)
│  { "matematicas": {               │
│       "potencia": <nodo AST>,     │
│       "factorial": <nodo AST>}    │
│  }                                 │
└─────────────┬─────────────────────┘
              │ (4) al evaluar matematicas.potencia(2,3)
              ▼
┌───────────────────────────────┐
│  Motor de ejecucion (Visitor)    │  ← el ArcanumVisitor.py ya generado
│  invoca el nodo AST de la        │     por ANTLR desde el Corte 1,
│  receta con un nuevo marco de    │     completandolo con logica real
│  variables locales                │
└───────────────────────────────┘
```

### Decisión de diseño clave

Se optó por un **intérprete de árbol (tree-walking interpreter)**
compartido entre el grimorio principal y los compendios, en lugar de
transpilar cada compendio a un módulo real de Python:

- Cumple el requisito de "librerías construidas desde cero": ni la
  resolución de nombres ni la ejecución de recetas dependen del sistema
  de `import` de Python.
- El motor de ejecución seguirá usando pandas/NumPy/Matplotlib **solo
  como backend de cálculo**, nunca como mecanismo de organización del
  propio lenguaje.
- Este diseño reutiliza directamente `ArcanumVisitor.py`, generado desde
  el Corte 1 con la bandera `-visitor` mencionada en el README, pero que
  todavía no tiene lógica adentro (queda vacío/heredado a propósito
  hasta que haya semántica real que ejecutar).

## 4. Impacto en la gramática (Corte 3)

Nuevas reglas que se añadirán a `Arcanum.g4` sin modificar las
existentes (extensión aditiva):

```ebnf
instruccionUsar      ::= "usar" "compendio" ID ";" ;
definicionReceta      ::= "receta" ID "(" listaParametrosReceta? ")" bloque ;
listaParametrosReceta ::= ID ( "," ID )* ;
bloque                ::= "{" hechizo* "}" ;
instruccionDevolver   ::= "devolver" expresion ";" ;
llamadaReceta         ::= ( ID "." )? ID "(" listaArgumentos? ")" ;
listaArgumentos       ::= expresion ( "," expresion )* ;
```

## 5. Cronograma de incorporación

| Corte | Qué se agrega del sistema de librerías |
|---|---|
| 1 (actual) | Solo diseño y diagrama (este documento) |
| 2 | Definición de `receta`/`devolver` dentro de un mismo archivo (funciones locales, sin `usar` todavía) |
| 3 | Instrucción `usar compendio nombre;`, Resolutor de Compendios, Tabla de Compendios, y al menos dos compendios propios (`matematicas.arc`, `estadistica.arc`) integrados al caso de estudio final |
