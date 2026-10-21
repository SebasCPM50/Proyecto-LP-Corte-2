# Generated from Arcanum.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ArcanumParser import ArcanumParser
else:
    from ArcanumParser import ArcanumParser

# This class defines a complete listener for a parse tree produced by ArcanumParser.
class ArcanumListener(ParseTreeListener):

    # Enter a parse tree produced by ArcanumParser#programa.
    def enterPrograma(self, ctx:ArcanumParser.ProgramaContext):
        pass

    # Exit a parse tree produced by ArcanumParser#programa.
    def exitPrograma(self, ctx:ArcanumParser.ProgramaContext):
        pass


    # Enter a parse tree produced by ArcanumParser#hechizo.
    def enterHechizo(self, ctx:ArcanumParser.HechizoContext):
        pass

    # Exit a parse tree produced by ArcanumParser#hechizo.
    def exitHechizo(self, ctx:ArcanumParser.HechizoContext):
        pass


    # Enter a parse tree produced by ArcanumParser#asignacion.
    def enterAsignacion(self, ctx:ArcanumParser.AsignacionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#asignacion.
    def exitAsignacion(self, ctx:ArcanumParser.AsignacionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#expresion.
    def enterExpresion(self, ctx:ArcanumParser.ExpresionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#expresion.
    def exitExpresion(self, ctx:ArcanumParser.ExpresionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#invocarExpr.
    def enterInvocarExpr(self, ctx:ArcanumParser.InvocarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#invocarExpr.
    def exitInvocarExpr(self, ctx:ArcanumParser.InvocarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#recolectarExpr.
    def enterRecolectarExpr(self, ctx:ArcanumParser.RecolectarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#recolectarExpr.
    def exitRecolectarExpr(self, ctx:ArcanumParser.RecolectarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#purificarExpr.
    def enterPurificarExpr(self, ctx:ArcanumParser.PurificarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#purificarExpr.
    def exitPurificarExpr(self, ctx:ArcanumParser.PurificarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#ordenarExpr.
    def enterOrdenarExpr(self, ctx:ArcanumParser.OrdenarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#ordenarExpr.
    def exitOrdenarExpr(self, ctx:ArcanumParser.OrdenarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#direccionOrden.
    def enterDireccionOrden(self, ctx:ArcanumParser.DireccionOrdenContext):
        pass

    # Exit a parse tree produced by ArcanumParser#direccionOrden.
    def exitDireccionOrden(self, ctx:ArcanumParser.DireccionOrdenContext):
        pass


    # Enter a parse tree produced by ArcanumParser#transmutarExpr.
    def enterTransmutarExpr(self, ctx:ArcanumParser.TransmutarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#transmutarExpr.
    def exitTransmutarExpr(self, ctx:ArcanumParser.TransmutarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#sanarExpr.
    def enterSanarExpr(self, ctx:ArcanumParser.SanarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#sanarExpr.
    def exitSanarExpr(self, ctx:ArcanumParser.SanarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#destilarExpr.
    def enterDestilarExpr(self, ctx:ArcanumParser.DestilarExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#destilarExpr.
    def exitDestilarExpr(self, ctx:ArcanumParser.DestilarExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#listaAgregaciones.
    def enterListaAgregaciones(self, ctx:ArcanumParser.ListaAgregacionesContext):
        pass

    # Exit a parse tree produced by ArcanumParser#listaAgregaciones.
    def exitListaAgregaciones(self, ctx:ArcanumParser.ListaAgregacionesContext):
        pass


    # Enter a parse tree produced by ArcanumParser#agregacion.
    def enterAgregacion(self, ctx:ArcanumParser.AgregacionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#agregacion.
    def exitAgregacion(self, ctx:ArcanumParser.AgregacionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#funcionAgregacion.
    def enterFuncionAgregacion(self, ctx:ArcanumParser.FuncionAgregacionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#funcionAgregacion.
    def exitFuncionAgregacion(self, ctx:ArcanumParser.FuncionAgregacionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#describirExpr.
    def enterDescribirExpr(self, ctx:ArcanumParser.DescribirExprContext):
        pass

    # Exit a parse tree produced by ArcanumParser#describirExpr.
    def exitDescribirExpr(self, ctx:ArcanumParser.DescribirExprContext):
        pass


    # Enter a parse tree produced by ArcanumParser#instruccionPreservar.
    def enterInstruccionPreservar(self, ctx:ArcanumParser.InstruccionPreservarContext):
        pass

    # Exit a parse tree produced by ArcanumParser#instruccionPreservar.
    def exitInstruccionPreservar(self, ctx:ArcanumParser.InstruccionPreservarContext):
        pass


    # Enter a parse tree produced by ArcanumParser#instruccionRevelar.
    def enterInstruccionRevelar(self, ctx:ArcanumParser.InstruccionRevelarContext):
        pass

    # Exit a parse tree produced by ArcanumParser#instruccionRevelar.
    def exitInstruccionRevelar(self, ctx:ArcanumParser.InstruccionRevelarContext):
        pass


    # Enter a parse tree produced by ArcanumParser#instruccionDescribir.
    def enterInstruccionDescribir(self, ctx:ArcanumParser.InstruccionDescribirContext):
        pass

    # Exit a parse tree produced by ArcanumParser#instruccionDescribir.
    def exitInstruccionDescribir(self, ctx:ArcanumParser.InstruccionDescribirContext):
        pass


    # Enter a parse tree produced by ArcanumParser#instruccionUsar.
    def enterInstruccionUsar(self, ctx:ArcanumParser.InstruccionUsarContext):
        pass

    # Exit a parse tree produced by ArcanumParser#instruccionUsar.
    def exitInstruccionUsar(self, ctx:ArcanumParser.InstruccionUsarContext):
        pass


    # Enter a parse tree produced by ArcanumParser#definicionReceta.
    def enterDefinicionReceta(self, ctx:ArcanumParser.DefinicionRecetaContext):
        pass

    # Exit a parse tree produced by ArcanumParser#definicionReceta.
    def exitDefinicionReceta(self, ctx:ArcanumParser.DefinicionRecetaContext):
        pass


    # Enter a parse tree produced by ArcanumParser#instruccionDevolver.
    def enterInstruccionDevolver(self, ctx:ArcanumParser.InstruccionDevolverContext):
        pass

    # Exit a parse tree produced by ArcanumParser#instruccionDevolver.
    def exitInstruccionDevolver(self, ctx:ArcanumParser.InstruccionDevolverContext):
        pass


    # Enter a parse tree produced by ArcanumParser#llamadaReceta.
    def enterLlamadaReceta(self, ctx:ArcanumParser.LlamadaRecetaContext):
        pass

    # Exit a parse tree produced by ArcanumParser#llamadaReceta.
    def exitLlamadaReceta(self, ctx:ArcanumParser.LlamadaRecetaContext):
        pass


    # Enter a parse tree produced by ArcanumParser#listaArgumentos.
    def enterListaArgumentos(self, ctx:ArcanumParser.ListaArgumentosContext):
        pass

    # Exit a parse tree produced by ArcanumParser#listaArgumentos.
    def exitListaArgumentos(self, ctx:ArcanumParser.ListaArgumentosContext):
        pass


    # Enter a parse tree produced by ArcanumParser#listaIds.
    def enterListaIds(self, ctx:ArcanumParser.ListaIdsContext):
        pass

    # Exit a parse tree produced by ArcanumParser#listaIds.
    def exitListaIds(self, ctx:ArcanumParser.ListaIdsContext):
        pass


    # Enter a parse tree produced by ArcanumParser#instruccionForjar.
    def enterInstruccionForjar(self, ctx:ArcanumParser.InstruccionForjarContext):
        pass

    # Exit a parse tree produced by ArcanumParser#instruccionForjar.
    def exitInstruccionForjar(self, ctx:ArcanumParser.InstruccionForjarContext):
        pass


    # Enter a parse tree produced by ArcanumParser#listaParametros.
    def enterListaParametros(self, ctx:ArcanumParser.ListaParametrosContext):
        pass

    # Exit a parse tree produced by ArcanumParser#listaParametros.
    def exitListaParametros(self, ctx:ArcanumParser.ListaParametrosContext):
        pass


    # Enter a parse tree produced by ArcanumParser#parametro.
    def enterParametro(self, ctx:ArcanumParser.ParametroContext):
        pass

    # Exit a parse tree produced by ArcanumParser#parametro.
    def exitParametro(self, ctx:ArcanumParser.ParametroContext):
        pass


    # Enter a parse tree produced by ArcanumParser#condicionParentesis.
    def enterCondicionParentesis(self, ctx:ArcanumParser.CondicionParentesisContext):
        pass

    # Exit a parse tree produced by ArcanumParser#condicionParentesis.
    def exitCondicionParentesis(self, ctx:ArcanumParser.CondicionParentesisContext):
        pass


    # Enter a parse tree produced by ArcanumParser#condicionComparacion.
    def enterCondicionComparacion(self, ctx:ArcanumParser.CondicionComparacionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#condicionComparacion.
    def exitCondicionComparacion(self, ctx:ArcanumParser.CondicionComparacionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#condicionO.
    def enterCondicionO(self, ctx:ArcanumParser.CondicionOContext):
        pass

    # Exit a parse tree produced by ArcanumParser#condicionO.
    def exitCondicionO(self, ctx:ArcanumParser.CondicionOContext):
        pass


    # Enter a parse tree produced by ArcanumParser#condicionY.
    def enterCondicionY(self, ctx:ArcanumParser.CondicionYContext):
        pass

    # Exit a parse tree produced by ArcanumParser#condicionY.
    def exitCondicionY(self, ctx:ArcanumParser.CondicionYContext):
        pass


    # Enter a parse tree produced by ArcanumParser#condicionNo.
    def enterCondicionNo(self, ctx:ArcanumParser.CondicionNoContext):
        pass

    # Exit a parse tree produced by ArcanumParser#condicionNo.
    def exitCondicionNo(self, ctx:ArcanumParser.CondicionNoContext):
        pass


    # Enter a parse tree produced by ArcanumParser#comparacion.
    def enterComparacion(self, ctx:ArcanumParser.ComparacionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#comparacion.
    def exitComparacion(self, ctx:ArcanumParser.ComparacionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#operadorComparacion.
    def enterOperadorComparacion(self, ctx:ArcanumParser.OperadorComparacionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#operadorComparacion.
    def exitOperadorComparacion(self, ctx:ArcanumParser.OperadorComparacionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#parentesis.
    def enterParentesis(self, ctx:ArcanumParser.ParentesisContext):
        pass

    # Exit a parse tree produced by ArcanumParser#parentesis.
    def exitParentesis(self, ctx:ArcanumParser.ParentesisContext):
        pass


    # Enter a parse tree produced by ArcanumParser#cadenaLiteral.
    def enterCadenaLiteral(self, ctx:ArcanumParser.CadenaLiteralContext):
        pass

    # Exit a parse tree produced by ArcanumParser#cadenaLiteral.
    def exitCadenaLiteral(self, ctx:ArcanumParser.CadenaLiteralContext):
        pass


    # Enter a parse tree produced by ArcanumParser#sumaResta.
    def enterSumaResta(self, ctx:ArcanumParser.SumaRestaContext):
        pass

    # Exit a parse tree produced by ArcanumParser#sumaResta.
    def exitSumaResta(self, ctx:ArcanumParser.SumaRestaContext):
        pass


    # Enter a parse tree produced by ArcanumParser#potencia.
    def enterPotencia(self, ctx:ArcanumParser.PotenciaContext):
        pass

    # Exit a parse tree produced by ArcanumParser#potencia.
    def exitPotencia(self, ctx:ArcanumParser.PotenciaContext):
        pass


    # Enter a parse tree produced by ArcanumParser#llamadaFuncion.
    def enterLlamadaFuncion(self, ctx:ArcanumParser.LlamadaFuncionContext):
        pass

    # Exit a parse tree produced by ArcanumParser#llamadaFuncion.
    def exitLlamadaFuncion(self, ctx:ArcanumParser.LlamadaFuncionContext):
        pass


    # Enter a parse tree produced by ArcanumParser#numero.
    def enterNumero(self, ctx:ArcanumParser.NumeroContext):
        pass

    # Exit a parse tree produced by ArcanumParser#numero.
    def exitNumero(self, ctx:ArcanumParser.NumeroContext):
        pass


    # Enter a parse tree produced by ArcanumParser#multDivMod.
    def enterMultDivMod(self, ctx:ArcanumParser.MultDivModContext):
        pass

    # Exit a parse tree produced by ArcanumParser#multDivMod.
    def exitMultDivMod(self, ctx:ArcanumParser.MultDivModContext):
        pass


    # Enter a parse tree produced by ArcanumParser#booleano.
    def enterBooleano(self, ctx:ArcanumParser.BooleanoContext):
        pass

    # Exit a parse tree produced by ArcanumParser#booleano.
    def exitBooleano(self, ctx:ArcanumParser.BooleanoContext):
        pass


    # Enter a parse tree produced by ArcanumParser#identificador.
    def enterIdentificador(self, ctx:ArcanumParser.IdentificadorContext):
        pass

    # Exit a parse tree produced by ArcanumParser#identificador.
    def exitIdentificador(self, ctx:ArcanumParser.IdentificadorContext):
        pass


    # Enter a parse tree produced by ArcanumParser#valorLiteral.
    def enterValorLiteral(self, ctx:ArcanumParser.ValorLiteralContext):
        pass

    # Exit a parse tree produced by ArcanumParser#valorLiteral.
    def exitValorLiteral(self, ctx:ArcanumParser.ValorLiteralContext):
        pass



del ArcanumParser