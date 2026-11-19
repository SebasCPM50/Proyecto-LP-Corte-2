from __future__ import annotations
from errores import ErrorSemantico

class ControlFlujo:
    def visitBloqueHechizos(self, ctx: ArcanumParser.BloqueHechizosContext):
        # Ejecuta secuencialmente los hechizos agrupados dentro de un bloque { ... }
        for hechizo in ctx.hechizo():
            self.visit(hechizo)
        return None

    def visitInstruccionSi(self, ctx: ArcanumParser.InstruccionSiContext):
        # Evalúa la condición booleana y ejecuta el bloque 'si' o el bloque 'sino'
        cumple = bool(self.visit(ctx.condicion()))
        if cumple:
            if ctx.bloqueSi:
                self.visit(ctx.bloqueSi)
        elif ctx.bloqueSino:
            self.visit(ctx.bloqueSino)
        return None

    def visitInstruccionMientras(self, ctx: ArcanumParser.InstruccionMientrasContext):
        # Ejecuta el bloque mientras la condición se mantenga verdadera
        max_iteraciones = self.max_iteraciones
        contador = 0
        while bool(self.visit(ctx.condicion())):
            contador += 1
            if contador > max_iteraciones:
                raise ErrorSemantico("Límite de iteraciones alcanzado en bucle 'mientras' (posible ciclo infinito)", ctx.start.line, ctx.start.column)
            self.visit(ctx.bloqueHechizos())
        return None

    def visitInstruccionPara(self, ctx: ArcanumParser.InstruccionParaContext):
        # Bucle funcional sobre colecciones o listas
        nombre_var = ctx.ID().getText()
        coleccion = self.visit(ctx.expresion())
        if not hasattr(coleccion, "__iter__"):
            raise ErrorSemantico(f"El elemento en 'para {nombre_var} en ...' no es iterable", ctx.start.line, ctx.start.column)

        for item in coleccion:
            if self._marcos_locales:
                self._marcos_locales[-1][nombre_var] = item
            else:
                self.tabla.definir(nombre_var, item)
            self.visit(ctx.bloqueHechizos())
        return None

