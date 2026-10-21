grammar Arcanum;

// =========================================================================
// REGLAS DEL PARSER (Sintaxis)
// =========================================================================

// Punto de entrada del programa: uno o más hechizos terminados en fin de archivo (EOF).
programa
    : hechizo+ EOF
    ;

// Cada hechizo (instrucción) puede ser una asignación a variable o una acción directa.
hechizo
    : asignacion
    | instruccionPreservar
    | instruccionRevelar
    | instruccionDescribir
    | instruccionUsar
    | definicionReceta
    | instruccionForjar
    ;

// Asignación clásica: <variable> = <expresión>;
asignacion
    : ID '=' expresion ';'
    ;

// Una expresión representa cualquier valor o transformación de datos.
expresion
    : invocarExpr
    | recolectarExpr
    | purificarExpr
    | ordenarExpr
    | transmutarExpr
    | sanarExpr
    | destilarExpr
    | describirExpr
    | expresionAritmetica
    ;

// 1. Carga de datos desde un archivo CSV:
//    ventas = invocar desde "csv/ventas.csv";
invocarExpr
    : INVOCAR DESDE CADENA
    ;

// 2. Selección de columnas de una poción:
//    reducida = recolectar [fecha, ciudad, total] de ventas;
recolectarExpr
    : RECOLECTAR '[' listaIds ']' DE ID
    ;

// 3. Filtrado de filas según condiciones lógicas:
//    filtradas = purificar ventas donde unidades > 0 y precio > 0;
purificarExpr
    : PURIFICAR ID DONDE condicion
    ;

// 4. Ordenamiento de una poción por columna (ascendente por defecto o descendente):
//    ordenadas = ordenar ventas por precio desc;
//    ordenadas = ordenar ventas por fecha;
ordenarExpr
    : ORDENAR ID POR ID ( direccionOrden )?
    ;

direccionOrden
    : ASC
    | DESC
    ;

// 5. Columnas calculadas (transmutación alquímica):
//    totales = transmutar ventas con total = unidades * precio;
transmutarExpr
    : TRANSMUTAR ID CON ID '=' expresionAritmetica
    ;

// 6. Tratamiento de datos faltantes (sanación alquímica):
//    limpias = sanar ventas descartar_nulos;
//    rellenas = sanar ventas llenar precio con 0;
sanarExpr
    : SANAR ID DESCARTAR_NULOS
    | SANAR ID LLENAR ID CON valorLiteral
    ;

// 7. Agrupamiento y agregaciones (destilación del elixir de datos):
//    resumen = destilar ventas por [ciudad] agregar suma(total) como ingreso, contar() como cantidad;
destilarExpr
    : ( DESTILAR | AGRUPAR ) ID POR '[' listaIds ']' AGREGAR listaAgregaciones
    ;

listaAgregaciones
    : agregacion (',' agregacion)*
    ;

agregacion
    : funcionAgregacion '(' ID? ')' ( COMO ID )?
    ;

funcionAgregacion
    : SUMA
    | MEDIA
    | MEDIANA
    | MINIMO
    | MAXIMO
    | DESVIACION
    | CONTAR
    ;

// 8. Estadísticas descriptivas como expresión para guardar en variable:
//    stats = describir ventas;
describirExpr
    : DESCRIBIR ID
    ;

// 9. Instrucción para exportar pociones a CSV:
//    preservar resumen en "salidas/resumen_ciudades.csv";
//    guardar resumen en "salidas/resumen_ciudades.csv";
instruccionPreservar
    : ( PRESERVAR | GUARDAR ) ID EN CADENA ';'
    ;

// 10. Instrucción para mostrar una muestra de la poción en consola:
//    revelar ventas;
//    mostrar ventas_limpias;
instruccionRevelar
    : ( REVELAR | MOSTRAR ) ID ';'
    ;

// 11. Instrucción para imprimir estadísticas descriptivas en consola:
//    describir ventas;
instruccionDescribir
    : DESCRIBIR ID ';'
    ;

// 12. Sistema de Compendios y Recetas (Librerías Propias creadas desde 0):
//     usar compendio matematicas;
instruccionUsar
    : USAR COMPENDIO ID ';'
    ;

// Definición de una receta (función propia del lenguaje):
// receta calcular_iva(subtotal) { devolver subtotal * 0.19; }
definicionReceta
    : RECETA ID '(' listaIds? ')' '{' hechizo* ( instruccionDevolver )? '}'
    ;

instruccionDevolver
    : DEVOLVER expresion ';'
    ;

// Llamada a una receta de un compendio o local:
// matematicas.potencia(2, 3)  o  calcular_iva(total)
llamadaReceta
    : ( ID '.' )? ID '(' listaArgumentos? ')'
    ;

listaArgumentos
    : expresion ( ',' expresion )*
    ;

// Lista de uno o más identificadores separados por coma:
listaIds
    : ID (',' ID)*
    ;

// Visualización (para Corte 3, reconocida sintácticamente desde Corte 1 y 2):
// forjar artefacto barras desde ventas con eje_x ciudad, eje_y precio, titulo "...";
instruccionForjar
    : FORJAR ARTEFACTO ID DESDE ID CON listaParametros ';'
    ;

listaParametros
    : parametro (',' parametro)*
    ;

parametro
    : EJE_X ID
    | EJE_Y ID
    | TITULO CADENA
    ;

// Condiciones booleanas recursivas con precedencia: NOT > AND > OR
condicion
    : condicion Y condicion              # condicionY
    | condicion O condicion              # condicionO
    | NO condicion                       # condicionNo
    | '(' condicion ')'                  # condicionParentesis
    | comparacion                        # condicionComparacion
    ;

comparacion
    : expresionAritmetica operadorComparacion expresionAritmetica
    ;

operadorComparacion
    : '>' | '<' | '>=' | '<=' | '==' | '!='
    ;

// Expresión aritmética con soporte de potencia (^), mult/div/mod (*, /, %) y suma/resta (+, -)
expresionAritmetica
    : expresionAritmetica '^' expresionAritmetica                 # potencia
    | expresionAritmetica ( '*' | '/' | '%' ) expresionAritmetica # multDivMod
    | expresionAritmetica ( '+' | '-' ) expresionAritmetica       # sumaResta
    | '(' expresionAritmetica ')'                                 # parentesis
    | llamadaReceta                                               # llamadaFuncion
    | NUMERO                                                      # numero
    | CADENA                                                      # cadenaLiteral
    | ( VERDADERO | FALSO )                                       # booleano
    | ID                                                          # identificador
    ;

valorLiteral
    : NUMERO
    | CADENA
    | VERDADERO
    | FALSO
    ;

// =========================================================================
// REGLAS DEL LEXER (Tokens)
// =========================================================================

// Palabras reservadas principales de Arcanum
INVOCAR          : 'invocar';
RECOLECTAR       : 'recolectar';
PURIFICAR        : 'purificar';
ORDENAR          : 'ordenar';
TRANSMUTAR       : 'transmutar';
SANAR            : 'sanar';
DESCARTAR_NULOS  : 'descartar_nulos';
LLENAR           : 'llenar';
DESTILAR         : 'destilar';
AGRUPAR          : 'agrupar';
AGREGAR          : 'agregar' | 'resumir';
COMO             : 'como';
PRESERVAR        : 'preservar';
GUARDAR          : 'guardar';
REVELAR          : 'revelar';
MOSTRAR          : 'mostrar';
DESCRIBIR        : 'describir';

// Compendios y recetas (sistema de librerías propio)
USAR             : 'usar';
COMPENDIO        : 'compendio';
RECETA           : 'receta';
DEVOLVER         : 'devolver';

// Funciones de agregación
SUMA             : 'suma';
MEDIA            : 'media' | 'promedio';
MEDIANA          : 'mediana';
MINIMO           : 'minimo' | 'min';
MAXIMO           : 'maximo' | 'max';
DESVIACION       : 'desviacion' | 'std';
CONTAR           : 'contar' | 'conteo';

// Ordenamiento
ASC              : 'asc' | 'ascendente';
DESC             : 'desc' | 'descendente';

// Visualización (para Corte 3, reconocida en Corte 1 y 2)
FORJAR           : 'forjar';
ARTEFACTO        : 'artefacto';
EJE_X            : 'eje_x';
EJE_Y            : 'eje_y';
TITULO           : 'titulo';

// Preposiciones y conectores
DESDE            : 'desde';
DE               : 'de';
DONDE            : 'donde';
CON              : 'con';
POR              : 'por';
EN               : 'en';

// Operadores lógicos
Y                : 'y';
O                : 'o';
NO               : 'no';

// Literales booleanos
VERDADERO        : 'verdadero';
FALSO            : 'falso';

// Identificadores (nombres de variables y columnas)
ID               : [a-zA-Z_][a-zA-Z0-9_]*;

// Literales numéricos (enteros y decimales)
NUMERO           : [0-9]+ ('.' [0-9]+)?;

// Cadenas de texto entre comillas dobles
CADENA           : '"' (~["\r\n])* '"';

// Comentarios de línea (inician con # hasta fin de línea)
COMENTARIO       : '#' ~[\r\n]* -> skip;

// Espacios en blanco y saltos de línea ignorados
ESPACIO          : [ \t\r\n]+ -> skip;
