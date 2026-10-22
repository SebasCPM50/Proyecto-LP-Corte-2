# Generated from Arcanum.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ArcanumParser import ArcanumParser
else:
    from ArcanumParser import ArcanumParser

# This class defines a complete generic visitor for a parse tree produced by ArcanumParser.

class ArcanumVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ArcanumParser#programa.
    def visitPrograma(self, ctx:ArcanumParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#hechizo.
    def visitHechizo(self, ctx:ArcanumParser.HechizoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#asignacion.
    def visitAsignacion(self, ctx:ArcanumParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#expresion.
    def visitExpresion(self, ctx:ArcanumParser.ExpresionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#invocarExpr.
    def visitInvocarExpr(self, ctx:ArcanumParser.InvocarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#recolectarExpr.
    def visitRecolectarExpr(self, ctx:ArcanumParser.RecolectarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#purificarExpr.
    def visitPurificarExpr(self, ctx:ArcanumParser.PurificarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#ordenarExpr.
    def visitOrdenarExpr(self, ctx:ArcanumParser.OrdenarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#direccionOrden.
    def visitDireccionOrden(self, ctx:ArcanumParser.DireccionOrdenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#transmutarExpr.
    def visitTransmutarExpr(self, ctx:ArcanumParser.TransmutarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#sanarExpr.
    def visitSanarExpr(self, ctx:ArcanumParser.SanarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#destilarExpr.
    def visitDestilarExpr(self, ctx:ArcanumParser.DestilarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#listaAgregaciones.
    def visitListaAgregaciones(self, ctx:ArcanumParser.ListaAgregacionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#agregacion.
    def visitAgregacion(self, ctx:ArcanumParser.AgregacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#funcionAgregacion.
    def visitFuncionAgregacion(self, ctx:ArcanumParser.FuncionAgregacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#describirExpr.
    def visitDescribirExpr(self, ctx:ArcanumParser.DescribirExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#instruccionPreservar.
    def visitInstruccionPreservar(self, ctx:ArcanumParser.InstruccionPreservarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#instruccionRevelar.
    def visitInstruccionRevelar(self, ctx:ArcanumParser.InstruccionRevelarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#instruccionDescribir.
    def visitInstruccionDescribir(self, ctx:ArcanumParser.InstruccionDescribirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#instruccionUsar.
    def visitInstruccionUsar(self, ctx:ArcanumParser.InstruccionUsarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#definicionReceta.
    def visitDefinicionReceta(self, ctx:ArcanumParser.DefinicionRecetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#instruccionDevolver.
    def visitInstruccionDevolver(self, ctx:ArcanumParser.InstruccionDevolverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#llamadaReceta.
    def visitLlamadaReceta(self, ctx:ArcanumParser.LlamadaRecetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#listaArgumentos.
    def visitListaArgumentos(self, ctx:ArcanumParser.ListaArgumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#listaIds.
    def visitListaIds(self, ctx:ArcanumParser.ListaIdsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#instruccionForjar.
    def visitInstruccionForjar(self, ctx:ArcanumParser.InstruccionForjarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#listaParametros.
    def visitListaParametros(self, ctx:ArcanumParser.ListaParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#parametro.
    def visitParametro(self, ctx:ArcanumParser.ParametroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#condicionParentesis.
    def visitCondicionParentesis(self, ctx:ArcanumParser.CondicionParentesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#condicionComparacion.
    def visitCondicionComparacion(self, ctx:ArcanumParser.CondicionComparacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#condicionO.
    def visitCondicionO(self, ctx:ArcanumParser.CondicionOContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#condicionY.
    def visitCondicionY(self, ctx:ArcanumParser.CondicionYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#condicionNo.
    def visitCondicionNo(self, ctx:ArcanumParser.CondicionNoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#comparacion.
    def visitComparacion(self, ctx:ArcanumParser.ComparacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#operadorComparacion.
    def visitOperadorComparacion(self, ctx:ArcanumParser.OperadorComparacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#parentesis.
    def visitParentesis(self, ctx:ArcanumParser.ParentesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#cadenaLiteral.
    def visitCadenaLiteral(self, ctx:ArcanumParser.CadenaLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#sumaResta.
    def visitSumaResta(self, ctx:ArcanumParser.SumaRestaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#potencia.
    def visitPotencia(self, ctx:ArcanumParser.PotenciaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#llamadaFuncion.
    def visitLlamadaFuncion(self, ctx:ArcanumParser.LlamadaFuncionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#numero.
    def visitNumero(self, ctx:ArcanumParser.NumeroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#multDivMod.
    def visitMultDivMod(self, ctx:ArcanumParser.MultDivModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#booleano.
    def visitBooleano(self, ctx:ArcanumParser.BooleanoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#identificador.
    def visitIdentificador(self, ctx:ArcanumParser.IdentificadorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArcanumParser#valorLiteral.
    def visitValorLiteral(self, ctx:ArcanumParser.ValorLiteralContext):
        return self.visitChildren(ctx)



del ArcanumParser