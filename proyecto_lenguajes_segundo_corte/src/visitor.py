"""
Módulo del Intérprete Semántico (Visitor) — Arcanum
Implementa el patrón de diseño Visitor generado por ANTLR4
Recorre el Árbol de Análisis Sintáctico y ejecuta cada instrucción

100% LIBRE DE LIBRERÍAS EXTERNAS:
- NO UTILIZA PANDAS NI NUMPY
- Utiliza la clase artesanal Pocion (src/pocion.py) construida con listas y diccionarios nativos
- Implementa compendios y recetas desde cero sin import de Python
"""

import os
import sys

# Agregamos la carpeta generated al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from antlr4 import FileStream, CommonTokenStream
from ArcanumLexer import ArcanumLexer
from ArcanumParser import ArcanumParser
from ArcanumVisitor import ArcanumVisitor
from errores import ErrorSemantico
from tabla_simbolos import TablaSimbolos
from pocion import Pocion
from motor import MotorDatos


class RecetaAlquimica:
    """
    Representa una función propia definida dentro del lenguaje Arcanum
    """
    def __init__(self, nombre, parametros, lista_hechizos, nodo_devolver):
        self.nombre = nombre
        self.parametros = parametros
        self.lista_hechizos = lista_hechizos
        self.nodo_devolver = nodo_devolver


class ArcanumVisitorEjecutor(ArcanumVisitor):
    """
    Intérprete principal de Arcanum
    """

    def __init__(self, tabla_simbolos=None):
        super().__init__()
        self.tabla = tabla_simbolos if tabla_simbolos is not None else TablaSimbolos()
        # Fila activa durante la evaluación de filtros o columnas calculadas
        self._fila_activa = None
        # Recetas locales definidas en este grimorio
        self._recetas_locales = {}
        # Compendios cargados con 'usar compendio'
        self._compendios = {}
        # Marcos de variables locales durante llamadas a recetas
        self._marcos_locales = []

    # =========================================================================
    # REGLAS ESTRUCTURALES
    # =========================================================================

    def visitPrograma(self, ctx: ArcanumParser.ProgramaContext):
        for hechizo in ctx.hechizo():
            self.visit(hechizo)
        return self.tabla

    def visitHechizo(self, ctx: ArcanumParser.HechizoContext):
        return self.visitChildren(ctx)

    def visitAsignacion(self, ctx: ArcanumParser.AsignacionContext):
        nombre_var = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        valor = self.visit(ctx.expresion())
        
        if self._marcos_locales:
            self._marcos_locales[-1][nombre_var] = valor
        else:
            self.tabla.definir(nombre_var, valor, linea=linea, columna=columna)
        return valor

    def visitExpresion(self, ctx: ArcanumParser.ExpresionContext):
        return self.visitChildren(ctx)

    # =========================================================================
    # OPERACIONES DEL DSL (CIENCIA DE DATOS ARTESANAL)
    # =========================================================================

    def visitInvocarExpr(self, ctx: ArcanumParser.InvocarExprContext):
        ruta_archivo = ctx.CADENA().getText().strip('"')
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = MotorDatos.cargar_csv(ruta_archivo, linea=linea, columna=columna)
        print(f"[Hechizo Invocado]: Poción cargada desde '{ruta_archivo}' ({len(pocion)} registros)")
        return pocion

    def visitRecolectarExpr(self, ctx: ArcanumParser.RecolectarExprContext):
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        columnas = [id_node.getText() for id_node in ctx.listaIds().ID()]
        self.tabla.verificar_columnas(nombre_pocion, columnas, linea=linea, columna=columna)
        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        resultado = MotorDatos.recolectar(pocion_origen, columnas)
        print(f"[Hechizo Recolección]: Se seleccionaron {columnas} de '{nombre_pocion}'")
        return resultado

    def visitPurificarExpr(self, ctx: ArcanumParser.PurificarExprContext):
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        def evaluador_condicion_fila(fila):
            antigua_fila = self._fila_activa
            self._fila_activa = fila
            try:
                res = self.visit(ctx.condicion())
                return bool(res)
            finally:
                self._fila_activa = antigua_fila

        resultado = MotorDatos.purificar(pocion_origen, evaluador_condicion_fila)
        descartadas = len(pocion_origen) - len(resultado)
        print(f"[Hechizo Purificación]: Poción '{nombre_pocion}' purificada ({len(resultado)} conservadas, {descartadas} descartadas)")
        return resultado

    def visitOrdenarExpr(self, ctx: ArcanumParser.OrdenarExprContext):
        nombre_pocion = ctx.ID(0).getText()
        columna_orden = ctx.ID(1).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        self.tabla.verificar_columna(nombre_pocion, columna_orden, linea=linea, columna=columna)
        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        ascendente = True
        if ctx.direccionOrden() and ctx.direccionOrden().DESC():
            ascendente = False

        resultado = MotorDatos.ordenar(pocion_origen, columna_orden, ascendente=ascendente)
        sentido = "ascendente" if ascendente else "descendente"
        print(f"[Hechizo Ordenamiento]: Poción '{nombre_pocion}' ordenada por '{columna_orden}' ({sentido})")
        return resultado

    def visitTransmutarExpr(self, ctx: ArcanumParser.TransmutarExprContext):
        nombre_pocion = ctx.ID(0).getText()
        columna_nueva = ctx.ID(1).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        def evaluador_expresion_fila(fila):
            antigua_fila = self._fila_activa
            self._fila_activa = fila
            try:
                return self.visit(ctx.expresionAritmetica())
            finally:
                self._fila_activa = antigua_fila

        resultado = MotorDatos.transmutar(pocion_origen, columna_nueva, evaluador_expresion_fila)
        print(f"[Hechizo Transmutación]: Nuevo ingrediente '{columna_nueva}' añadido a '{nombre_pocion}'")
        return resultado

    def visitSanarExpr(self, ctx: ArcanumParser.SanarExprContext):
        nombre_pocion = ctx.ID(0).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        if ctx.DESCARTAR_NULOS():
            resultado = MotorDatos.sanar_descartar_nulos(pocion_origen)
            removidas = len(pocion_origen) - len(resultado)
            print(f"[Hechizo Sanación]: Poción '{nombre_pocion}' sanada descartando nulos ({removidas} filas removidas)")
            return resultado
        else:
            columna_objetivo = ctx.ID(1).getText()
            self.tabla.verificar_columna(nombre_pocion, columna_objetivo, linea=linea, columna=columna)
            valor_relleno = self.visit(ctx.valorLiteral())
            resultado = MotorDatos.sanar_llenar_nulos(pocion_origen, columna_objetivo, valor_relleno)
            print(f"[Hechizo Sanación]: Nulos en '{columna_objetivo}' de '{nombre_pocion}' rellenados con '{valor_relleno}'")
            return resultado

    def visitDestilarExpr(self, ctx: ArcanumParser.DestilarExprContext):
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        cols_grupo = [id_node.getText() for id_node in ctx.listaIds().ID()]
        self.tabla.verificar_columnas(nombre_pocion, cols_grupo, linea=linea, columna=columna)
        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        lista_agregaciones = []
        for ag_ctx in ctx.listaAgregaciones().agregacion():
            fn_nombre = ag_ctx.funcionAgregacion().getText().lower()
            ids = ag_ctx.ID()
            col_ag = None
            alias_ag = None

            if len(ids) == 2:
                col_ag = ids[0].getText()
                alias_ag = ids[1].getText()
            elif len(ids) == 1:
                if fn_nombre in ["contar", "conteo"]:
                    alias_ag = ids[0].getText()
                else:
                    col_ag = ids[0].getText()
                    alias_ag = f"{fn_nombre}_{col_ag}"
            else:
                alias_ag = "cantidad"

            if col_ag:
                self.tabla.verificar_columna(nombre_pocion, col_ag, linea=ag_ctx.start.line, columna=ag_ctx.start.column)

            lista_agregaciones.append({
                "funcion": fn_nombre,
                "columna": col_ag,
                "alias": alias_ag
            })

        resultado = MotorDatos.destilar(pocion_origen, cols_grupo, lista_agregaciones)
        print(f"[Hechizo Destilación]: Resumen generado agrupando por {cols_grupo} ({len(resultado)} filas resultantes)")
        return resultado

    def visitDescribirExpr(self, ctx: ArcanumParser.DescribirExprContext):
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        return MotorDatos.describir(pocion)

    def visitInstruccionDescribir(self, ctx: ArcanumParser.InstruccionDescribirContext):
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        print()
        print(f"[ESTADÍSTICAS DESCRIPTIVAS DE '{nombre_pocion}']")
        resumen = MotorDatos.describir(pocion)
        resumen.mostrar()
        print()
        return None

    def visitInstruccionRevelar(self, ctx: ArcanumParser.InstruccionRevelarContext):
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        print()
        print(f"[REVELACIÓN DE LA POCIÓN '{nombre_pocion}']")
        print(f"Dimensiones: {len(pocion)} registros x {len(pocion.columnas)} ingredientes")
        print(f"Ingredientes: {pocion.columnas}")
        print()
        pocion.mostrar()
        print()
        return None

    def visitInstruccionPreservar(self, ctx: ArcanumParser.InstruccionPreservarContext):
        nombre_pocion = ctx.ID().getText()
        ruta_salida = ctx.CADENA().getText().strip('"')
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        MotorDatos.guardar_csv(pocion, ruta_salida, linea=linea, columna=columna)
        print(f"[Hechizo Preservación]: Poción '{nombre_pocion}' exportada a '{ruta_salida}' ({len(pocion)} filas)")
        return None

    def visitInstruccionForjar(self, ctx: ArcanumParser.InstruccionForjarContext):
        tipo_artefacto = ctx.ID(0).getText()
        origen = ctx.ID(1).getText()
        print(f"[Hechizo de Forja reconocido]: Se preparará artefacto visual '{tipo_artefacto}' desde '{origen}' (reservado para Corte 3)")
        return None

    # =========================================================================
    # COMPENDIOS Y RECETAS (LIBRERÍAS PROPIAS)
    # =========================================================================

    def visitInstruccionUsar(self, ctx: ArcanumParser.InstruccionUsarContext):
        nombre_compendio = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        ruta_compendio = os.path.join("compendios", f"{nombre_compendio}.arc")
        if not os.path.exists(ruta_compendio):
            ruta_compendio = os.path.join(os.path.dirname(__file__), "..", "compendios", f"{nombre_compendio}.arc")
        
        if not os.path.exists(ruta_compendio):
            raise ErrorSemantico(
                f"No se encontró el compendio '{nombre_compendio}' en 'compendios/{nombre_compendio}.arc'",
                linea, columna
            )

        entrada = FileStream(ruta_compendio, encoding="utf-8")
        lexer = ArcanumLexer(entrada)
        tokens = CommonTokenStream(lexer)
        parser = ArcanumParser(tokens)
        arbol = parser.programa()

        sub_visitor = ArcanumVisitorEjecutor(self.tabla)
        sub_visitor.visit(arbol)
        self._compendios[nombre_compendio] = sub_visitor._recetas_locales

        print(f"[Compendio Cargado]: Librería propia '{nombre_compendio}' cargada desde '{ruta_compendio}' ({len(sub_visitor._recetas_locales)} recetas disponibles)")
        return None

    def visitDefinicionReceta(self, ctx: ArcanumParser.DefinicionRecetaContext):
        nombre = ctx.ID().getText()
        parametros = [id_n.getText() for id_n in ctx.listaIds().ID()] if ctx.listaIds() else []
        hechizos = ctx.hechizo()
        nodo_devolver = ctx.instruccionDevolver()

        receta = RecetaAlquimica(nombre, parametros, hechizos, nodo_devolver)
        self._recetas_locales[nombre] = receta
        return None

    def visitLlamadaFuncion(self, ctx: ArcanumParser.LlamadaFuncionContext):
        return self.visit(ctx.llamadaReceta())

    def visitLlamadaReceta(self, ctx: ArcanumParser.LlamadaRecetaContext):
        ids = ctx.ID()
        linea = ctx.start.line
        columna = ctx.start.column

        if len(ids) == 2:
            compendio_nom = ids[0].getText()
            receta_nom = ids[1].getText()
            if compendio_nom not in self._compendios:
                raise ErrorSemantico(f"El compendio '{compendio_nom}' no ha sido cargado con 'usar compendio {compendio_nom};'", linea, columna)
            if receta_nom not in self._compendios[compendio_nom]:
                raise ErrorSemantico(f"La receta '{receta_nom}' no existe en el compendio '{compendio_nom}'", linea, columna)
            receta = self._compendios[compendio_nom][receta_nom]
        else:
            receta_nom = ids[0].getText()
            if receta_nom in self._recetas_locales:
                receta = self._recetas_locales[receta_nom]
            else:
                encontrada = None
                for c_nom, c_dict in self._compendios.items():
                    if receta_nom in c_dict:
                        encontrada = c_dict[receta_nom]
                        break
                if not encontrada:
                    raise ErrorSemantico(f"La receta o función '{receta_nom}' no ha sido definida", linea, columna)
                receta = encontrada

        argumentos = []
        if ctx.listaArgumentos():
            for expr_arg in ctx.listaArgumentos().expresion():
                argumentos.append(self.visit(expr_arg))

        if len(argumentos) != len(receta.parametros):
            raise ErrorSemantico(
                f"La receta '{receta.nombre}' espera {len(receta.parametros)} ingredientes (argumentos), pero recibió {len(argumentos)}",
                linea, columna
            )

        marco_local = dict(zip(receta.parametros, argumentos))
        self._marcos_locales.append(marco_local)

        try:
            for h in receta.lista_hechizos:
                self.visit(h)
            if receta.nodo_devolver:
                return self.visit(receta.nodo_devolver.expresion())
            return None
        finally:
            self._marcos_locales.pop()

    # =========================================================================
    # CONDICIONES Y COMPARACIONES
    # =========================================================================

    def visitCondicionY(self, ctx: ArcanumParser.CondicionYContext):
        izq = self.visit(ctx.condicion(0))
        der = self.visit(ctx.condicion(1))
        return bool(izq and der)

    def visitCondicionO(self, ctx: ArcanumParser.CondicionOContext):
        izq = self.visit(ctx.condicion(0))
        der = self.visit(ctx.condicion(1))
        return bool(izq or der)

    def visitCondicionNo(self, ctx: ArcanumParser.CondicionNoContext):
        val = self.visit(ctx.condicion())
        return not bool(val)

    def visitCondicionParentesis(self, ctx: ArcanumParser.CondicionParentesisContext):
        return self.visit(ctx.condicion())

    def visitCondicionComparacion(self, ctx: ArcanumParser.CondicionComparacionContext):
        return self.visit(ctx.comparacion())

    def visitComparacion(self, ctx: ArcanumParser.ComparacionContext):
        izq = self.visit(ctx.expresionAritmetica(0))
        der = self.visit(ctx.expresionAritmetica(1))
        operador = ctx.operadorComparacion().getText()

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

    # =========================================================================
    # EXPRESIONES ARITMÉTICAS Y VALORES
    # =========================================================================

    def visitPotencia(self, ctx: ArcanumParser.PotenciaContext):
        izq = self.visit(ctx.expresionAritmetica(0))
        der = self.visit(ctx.expresionAritmetica(1))
        self._validar_operacion_numerica(izq, der, "^", ctx.start.line, ctx.start.column)
        return izq ** der

    def visitMultDivMod(self, ctx: ArcanumParser.MultDivModContext):
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
        if not (isinstance(izq, (int, float)) and isinstance(der, (int, float))):
            raise ErrorSemantico(
                f"La operación aritmética '{op}' solo es permitida entre valores numéricos ({type(izq).__name__} y {type(der).__name__})",
                linea, columna
            )

    def visitParentesis(self, ctx: ArcanumParser.ParentesisContext):
        return self.visit(ctx.expresionAritmetica())

    def visitNumero(self, ctx: ArcanumParser.NumeroContext):
        texto = ctx.getText()
        return float(texto) if '.' in texto else int(texto)

    def visitCadenaLiteral(self, ctx: ArcanumParser.CadenaLiteralContext):
        return ctx.getText().strip('"')

    def visitBooleano(self, ctx: ArcanumParser.BooleanoContext):
        return True if ctx.VERDADERO() else False

    def visitValorLiteral(self, ctx: ArcanumParser.ValorLiteralContext):
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
        nombre = ctx.getText()
        linea = ctx.start.line
        columna = ctx.start.column

        # 1. Si estamos dentro de una función local y existe el parámetro/variable
        if self._marcos_locales and nombre in self._marcos_locales[-1]:
            return self._marcos_locales[-1][nombre]

        # 2. Si estamos dentro de purificar o transmutar y coincide con una columna de la fila activa
        if self._fila_activa is not None and nombre in self._fila_activa:
            return self._fila_activa[nombre]

        # 3. Si existe en la tabla de símbolos global
        if self.tabla.existe(nombre):
            return self.tabla.obtener_valor(nombre, linea, columna)

        # Si no se encuentra en ningún ámbito
        if self._fila_activa is not None:
            cols = list(self._fila_activa.keys())
            raise ErrorSemantico(
                f"El ingrediente '{nombre}' no existe en la poción activa ni como variable declarada (Disponibles: {cols})",
                linea, columna
            )
        else:
            raise ErrorSemantico(
                f"La variable o ingrediente '{nombre}' no ha sido declarada o invocada previamente",
                linea, columna
            )
