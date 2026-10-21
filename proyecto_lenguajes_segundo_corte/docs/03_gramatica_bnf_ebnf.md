# Gramática Formal BNF / EBNF — Arcanum (Segundo Corte)

Este documento describe la especificación sintáctica formal del lenguaje Arcanum en notación EBNF (*Extended Backus-Naur Form*), actualizada para el Segundo Corte.

---

## 1. Notación EBNF utilizada
- `::=` define una regla de producción.
- `|` indica alternativa (o).
- `[ ... ]` indica elemento opcional (cero o una vez).
- `{ ... }` indica repetición (cero o más veces).
- `( ... )` agrupa elementos.
- Los terminales literales van entre comillas simples: `'invocar'`, `';'`, `'='`.
- Los terminales del lexer van en mayúsculas: `ID`, `NUMERO`, `CADENA`.

---

## 2. Reglas del Parser (EBNF)

```ebnf
(* Programa principal *)
programa            ::= { hechizo }+ EOF ;

(* Instrucciones posibles *)
hechizo             ::= asignacion
                      | instruccionPreservar
                      | instruccionRevelar
                      | instruccionDescribir
                      | instruccionForjar ;

(* Asignación a variable *)
asignacion          ::= ID '=' expresion ';' ;

(* Expresiones *)
expresion           ::= invocarExpr
                      | recolectarExpr
                      | purificarExpr
                      | ordenarExpr
                      | transmutarExpr
                      | sanarExpr
                      | destilarExpr
                      | describirExpr
                      | expresionAritmetica ;

(* Operaciones del DSL *)
invocarExpr         ::= 'invocar' 'desde' CADENA ;

recolectarExpr      ::= 'recolectar' '[' listaIds ']' 'de' ID ;

purificarExpr       ::= 'purificar' ID 'donde' condicion ;

ordenarExpr         ::= 'ordenar' ID 'por' ID [ direccionOrden ] ;
direccionOrden      ::= 'asc' | 'ascendente' | 'desc' | 'descendente' ;

transmutarExpr      ::= 'transmutar' ID 'con' ID '=' expresionAritmetica ;

sanarExpr           ::= 'sanar' ID 'descartar_nulos'
                      | 'sanar' ID 'llenar' ID 'con' valorLiteral ;

destilarExpr        ::= ( 'destilar' | 'agrupar' ) ID 'por' '[' listaIds ']' 'agregar' listaAgregaciones ;
listaAgregaciones   ::= agregacion { ',' agregacion } ;
agregacion          ::= funcionAgregacion '(' [ ID ] ')' [ 'como' ID ] ;
funcionAgregacion   ::= 'suma' | 'media' | 'promedio' | 'mediana' 
                      | 'minimo' | 'min' | 'maximo' | 'max' 
                      | 'desviacion' | 'std' | 'contar' | 'conteo' ;

describirExpr       ::= 'describir' ID ;

(* Instrucciones directas *)
instruccionPreservar ::= ( 'preservar' | 'guardar' ) ID 'en' CADENA ';' ;
instruccionRevelar   ::= ( 'revelar' | 'mostrar' ) ID ';' ;
instruccionDescribir ::= 'describir' ID ';' ;

instruccionForjar    ::= 'forjar' 'artefacto' ID 'desde' ID 'con' listaParametros ';' ;
listaParametros      ::= parametro { ',' parametro } ;
parametro            ::= 'eje_x' ID
                       | 'eje_y' ID
                       | 'titulo' CADENA ;

listaIds            ::= ID { ',' ID } ;

(* Condiciones y comparaciones *)
condicion           ::= condicion 'y' condicion
                      | condicion 'o' condicion
                      | 'no' condicion
                      | '(' condicion ')'
                      | comparacion ;

comparacion         ::= expresionAritmetica operadorComparacion expresionAritmetica ;
operadorComparacion ::= '>' | '<' | '>=' | '<=' | '==' | '!=' ;

(* Expresiones aritméticas *)
expresionAritmetica ::= expresionAritmetica '^' expresionAritmetica
                      | expresionAritmetica ( '*' | '/' | '%' ) expresionAritmetica
                      | expresionAritmetica ( '+' | '-' ) expresionAritmetica
                      | '(' expresionAritmetica ')'
                      | NUMERO
                      | CADENA
                      | ( 'verdadero' | 'falso' )
                      | ID ;

valorLiteral        ::= NUMERO | CADENA | 'verdadero' | 'falso' ;
```

---

## 3. Tokens del Lexer

```ebnf
ID         ::= [a-zA-Z_][a-zA-Z0-9_]* ;
NUMERO     ::= [0-9]+ ( '.' [0-9]+ )? ;
CADENA     ::= '"' [^"\r\n]* '"' ;
COMENTARIO ::= '#' [^\r\n]* ;
ESPACIO    ::= [ \t\r\n]+ ;
```
