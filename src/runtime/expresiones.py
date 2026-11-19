from __future__ import annotations
from errores import ErrorSemantico

class Expresiones:
    def visitCondicionY(self, ctx: ArcanumParser.CondicionYContext):
        # Operador lógico Y (ambas condiciones deben ser verdaderas)
        return bool(self.visit(ctx.condicion(0))) and bool(self.visit(ctx.condicion(1)))

    def visitCondicionO(self, ctx: ArcanumParser.CondicionOContext):
        # Operador lógico O (con que una sea verdadera ya pasa)
        return bool(self.visit(ctx.condicion(0))) or bool(self.visit(ctx.condicion(1)))

    def visitCondicionNo(self, ctx: ArcanumParser.CondicionNoContext):
        # Niega la condición
        val = self.visit(ctx.condicion())
        return not bool(val)

    def visitCondicionParentesis(self, ctx: ArcanumParser.CondicionParentesisContext):
        # Respeta el orden de los paréntesis
        return self.visit(ctx.condicion())

    def visitCondicionComparacion(self, ctx: ArcanumParser.CondicionComparacionContext):
        # Resuelve la comparación entre dos expresiones
        return self.visit(ctx.comparacion())

    def visitComparacion(self, ctx: ArcanumParser.ComparacionContext):
        # Evalúa comparaciones matemáticas como >, <, >=, <=, == o !=
        izq = self.visit(ctx.expresionAritmetica(0))
        der = self.visit(ctx.expresionAritmetica(1))
        operador = ctx.operadorComparacion().getText()

        # Si alguno de los dos valores es None manejamos la igualdad de forma segura
        if izq is None or der is None:
            if operador == '==':
                return izq == der
            elif operador == '!=':
                return izq != der
            return False

        if operador == '>':
            return izq > der
        elif operador == '<':
            return izq < der
        elif operador == '>=':
            return izq >= der
        elif operador == '<=':
            return izq <= der
        elif operador == '==':
            return izq == der
        elif operador == '!=':
            return izq != der
        else:
            raise ErrorSemantico(f"Operador de comparación desconocido: '{operador}'", ctx.start.line, ctx.start.column)

    # Expresiones aritméticas y números

    def visitPotencia(self, ctx: ArcanumParser.PotenciaContext):
        # Eleva un número a la potencia de otro
        izq = self.visit(ctx.expresionAritmetica(0))
        der = self.visit(ctx.expresionAritmetica(1))
        self._validar_operacion_numerica(izq, der, "^", ctx.start.line, ctx.start.column)
        return izq ** der

    def visitMultDivMod(self, ctx: ArcanumParser.MultDivModContext):
        # Multiplica, divide o calcula el módulo revisando que no se divida entre cero
        izq = self.visit(ctx.expresionAritmetica(0))
        der = self.visit(ctx.expresionAritmetica(1))
        op = ctx.getChild(1).getText()

        self._validar_operacion_numerica(izq, der, op, ctx.start.line, ctx.start.column)

        if op == '*':
            return izq * der
        elif op == '/':
            if der == 0:
                raise ErrorSemantico("División por cero no permitida", ctx.start.line, ctx.start.column)
            return izq / der
        elif op == '%':
            if der == 0:
                raise ErrorSemantico("Operación módulo con divisor cero no permitida", ctx.start.line, ctx.start.column)
            return izq % der

    def visitSumaResta(self, ctx: ArcanumParser.SumaRestaContext):
        # Suma o resta dos valores, o concatena si alguno es texto
        izq = self.visit(ctx.expresionAritmetica(0))
        der = self.visit(ctx.expresionAritmetica(1))
        op = ctx.getChild(1).getText()

        if op == '+':
            if isinstance(izq, str) or isinstance(der, str):
                return str(izq) + str(der)
            self._validar_operacion_numerica(izq, der, "+", ctx.start.line, ctx.start.column)
            return izq + der
        elif op == '-':
            self._validar_operacion_numerica(izq, der, "-", ctx.start.line, ctx.start.column)
            return izq - der

    def _validar_operacion_numerica(self, izq, der, op, linea, columna):
        # Revisa que ambos lados sean números para que no intenten restar texto
        if not (isinstance(izq, (int, float)) and isinstance(der, (int, float))):
            raise ErrorSemantico(
                f"La operación aritmética '{op}' solo es permitida entre valores numéricos ({type(izq).__name__} y {type(der).__name__})",
                linea, columna
            )

    def visitParentesis(self, ctx: ArcanumParser.ParentesisContext):
        # Resuelve lo que esté adentro de los paréntesis primero
        return self.visit(ctx.expresionAritmetica())

    def visitListaLit(self, ctx: ArcanumParser.ListaLitContext):
        # Visita la regla de lista literal
        return self.visit(ctx.listaLiteral())

    def visitListaLiteral(self, ctx: ArcanumParser.ListaLiteralContext):
        # Construye un Arreglo funcional con los elementos evaluados
        from estructuras.arreglo import Arreglo
        elementos = [self.visit(e) for e in ctx.expresionAritmetica()] if ctx.expresionAritmetica() else []
        return Arreglo(elementos)

    def visitIndexacion(self, ctx: ArcanumParser.IndexacionContext):
        # Acceso por índice a una lista o matriz: objeto[indice]
        coleccion = self.visit(ctx.expresionAritmetica(0))
        indice = self.visit(ctx.expresionAritmetica(1))
        if isinstance(indice, bool) or not isinstance(indice, int):
            raise ErrorSemantico("El índice debe ser un número entero", ctx.start.line, ctx.start.column)
        try:
            return coleccion[indice]
        except Exception as e:
            raise ErrorSemantico(f"Error al indexar en [{indice}]: {str(e)}", ctx.start.line, ctx.start.column)

    def visitNumero(self, ctx: ArcanumParser.NumeroContext):
        # Convierte el texto del token a int o float
        texto = ctx.getText()
        return float(texto) if '.' in texto else int(texto)

    def visitCadenaLiteral(self, ctx: ArcanumParser.CadenaLiteralContext):
        # Quita las comillas de la cadena de texto
        return ctx.getText().strip('"')

    def visitBooleano(self, ctx: ArcanumParser.BooleanoContext):
        # Retorna el booleano nativo de Python True o False
        return True if ctx.VERDADERO() else False

    def visitValorLiteral(self, ctx: ArcanumParser.ValorLiteralContext):
        # Convierte cualquier valor literal a su tipo correspondiente
        if ctx.NUMERO():
            texto = ctx.NUMERO().getText()
            return float(texto) if '.' in texto else int(texto)
        elif ctx.CADENA():
            return ctx.CADENA().getText().strip('"')
        elif ctx.VERDADERO():
            return True
        elif ctx.FALSO():
            return False
        return self.visitChildren(ctx)

    def visitIdentificador(self, ctx: ArcanumParser.IdentificadorContext):
        # Resuelve el valor de una variable buscando en orden de prioridad:
        nombre = ctx.getText()
        linea = ctx.start.line
        columna = ctx.start.column

        return self.obtener_valor(nombre, linea, columna)

    def visitNegativo(self, ctx):
        valor = self.visit(ctx.expresionAritmetica())
        self._validar_operacion_numerica(valor, 0, "-", ctx.start.line, ctx.start.column)
        return -valor

    def visitCondicionValor(self, ctx):
        return bool(self.visit(ctx.expresionAritmetica()))
