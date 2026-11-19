"""
Intérprete semántico con el patrón Visitor para Arcanum
Acá recorremos el árbol de análisis sintáctico que generó ANTLR
y ejecutamos cada instrucción una por una usando nuestra clase artesanal Pocion
No usamos Pandas ni NumPy ni import de Python para compendios
"""

import os
import sys

# Agregamos las carpetas src y generated para imports modulares limpios
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

from ArcanumParser import ArcanumParser
from ArcanumVisitor import ArcanumVisitor
from errores import ErrorSemantico
from tabla_simbolos import TablaSimbolos
from pocion import Pocion
from motor import MotorDatos


from runtime.control import ControlFlujo
from runtime.expresiones import Expresiones
from runtime.recetas import Recetas
from runtime.ambitos import Ambitos
from runtime.nativas import crear_registro


class ArcanumVisitorEjecutor(ControlFlujo, Expresiones, Recetas, Ambitos, ArcanumVisitor):
    """
    Clase principal que recorre los nodos del árbol y va ejecutando el código de Arcanum
    """

    def __init__(self, tabla_simbolos=None, max_iteraciones=10000):
        super().__init__()
        # Si nos pasan una tabla de símbolos la usamos, si no creamos una limpia
        self.tabla = tabla_simbolos if tabla_simbolos is not None else TablaSimbolos()
        # Guarda la fila sobre la que estamos operando cuando hacemos filtros o cálculos
        self._fila_activa = None
        # Diccionario para guardar las recetas creadas en este archivo
        self._recetas_locales = {}
        # Diccionario para guardar las recetas cargadas con 'usar compendio'
        self._compendios = {}
        # Pila de memoria local para que las recetas tengan sus propias variables sin chocar
        self._marcos_locales = []
        self.max_iteraciones = max_iteraciones
        self._nativas = crear_registro()

    # Métodos estructurales del programa

    def visitPrograma(self, ctx: ArcanumParser.ProgramaContext):
        # Recorre cada hechizo del programa en orden de arriba a abajo
        for hechizo in ctx.hechizo():
            self.visit(hechizo)
        return self.tabla

    def visitHechizo(self, ctx: ArcanumParser.HechizoContext):
        # Simplemente delega en la instrucción concreta que corresponda
        return self.visitChildren(ctx)

    def visitAsignacion(self, ctx: ArcanumParser.AsignacionContext):
        # Acá evaluamos el valor a la derecha del igual y lo guardamos en la variable
        nombre_var = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        valor = self.visit(ctx.expresion())
        
        # Si estamos dentro de una receta lo guardamos en la memoria local de la función
        if self._marcos_locales:
            self._marcos_locales[-1][nombre_var] = valor
        else:
            # Si estamos en el programa principal lo guardamos en la tabla de símbolos global
            self.tabla.definir(nombre_var, valor, linea=linea, columna=columna)
        return valor

    # Control de flujo (condicionales y bucles)

    def visitExpresion(self, ctx: ArcanumParser.ExpresionContext):
        # Visita la expresión que corresponda
        return self.visitChildren(ctx)

    # Operaciones analíticas del lenguaje

    def visitInvocarExpr(self, ctx: ArcanumParser.InvocarExprContext):
        # Carga un archivo CSV desde la ruta indicada y devuelve una Poción nueva
        ruta_archivo = ctx.CADENA().getText().strip('"')
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = MotorDatos.cargar_csv(ruta_archivo, linea=linea, columna=columna)
        print(f"[Hechizo Invocado]: Poción cargada desde '{ruta_archivo}' ({len(pocion)} registros)")
        return pocion

    def visitRecolectarExpr(self, ctx: ArcanumParser.RecolectarExprContext):
        # Selecciona solo las columnas pedidas y valida que existan en la tabla
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        columnas = [id_node.getText() for id_node in ctx.listaIds().ID()]
        self.verificar_columnas(nombre_pocion, columnas, linea=linea, columna=columna)
        pocion_origen = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        resultado = MotorDatos.recolectar(pocion_origen, columnas)
        print(f"[Hechizo Recolección]: Se seleccionaron {columnas} de '{nombre_pocion}'")
        return resultado

    def visitPurificarExpr(self, ctx: ArcanumParser.PurificarExprContext):
        # Filtra las filas evaluando la condición para cada registro de la tabla
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        def evaluador_condicion_fila(fila):
            # Activamos temporalmente esta fila para que las comparaciones lean sus columnas
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
        # Ordena los datos de menor a mayor o de mayor a menor según la columna indicada
        nombre_pocion = ctx.ID(0).getText()
        columna_orden = ctx.ID(1).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        self.verificar_columna(nombre_pocion, columna_orden, linea=linea, columna=columna)
        pocion_origen = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        ascendente = True
        if ctx.direccionOrden() and ctx.direccionOrden().DESC():
            ascendente = False

        resultado = MotorDatos.ordenar(pocion_origen, columna_orden, ascendente=ascendente)
        sentido = "ascendente" if ascendente else "descendente"
        print(f"[Hechizo Ordenamiento]: Poción '{nombre_pocion}' ordenada por '{columna_orden}' ({sentido})")
        return resultado

    def visitTransmutarExpr(self, ctx: ArcanumParser.TransmutarExprContext):
        # Agrega una columna calculando una fórmula matemática fila por fila
        nombre_pocion = ctx.ID(0).getText()
        columna_nueva = ctx.ID(1).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        def evaluador_expresion_fila(fila):
            # Activamos la fila actual para que la fórmula pueda leer los valores de las columnas
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
        # Limpia los datos nulos ya sea botando la fila o rellenándola con un valor por defecto
        nombre_pocion = ctx.ID(0).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        if ctx.DESCARTAR_NULOS():
            resultado = MotorDatos.sanar_descartar_nulos(pocion_origen)
            removidas = len(pocion_origen) - len(resultado)
            print(f"[Hechizo Sanación]: Poción '{nombre_pocion}' sanada descartando nulos ({removidas} filas removidas)")
            return resultado
        else:
            columna_objetivo = ctx.ID(1).getText()
            self.verificar_columna(nombre_pocion, columna_objetivo, linea=linea, columna=columna)
            valor_relleno = self.visit(ctx.valorLiteral())
            resultado = MotorDatos.sanar_llenar_nulos(pocion_origen, columna_objetivo, valor_relleno)
            print(f"[Hechizo Sanación]: Nulos en '{columna_objetivo}' de '{nombre_pocion}' rellenados con '{valor_relleno}'")
            return resultado

    def visitDestilarExpr(self, ctx: ArcanumParser.DestilarExprContext):
        # Agrupa filas por categorías y calcula métricas como promedios o sumas
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        cols_grupo = [id_node.getText() for id_node in ctx.listaIds().ID()]
        self.verificar_columnas(nombre_pocion, cols_grupo, linea=linea, columna=columna)
        pocion_origen = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        # Extraemos la lista de funciones que nos pidieron calcular
        lista_agregaciones = []
        for ag_ctx in ctx.listaAgregaciones().agregacion():
            fn_nombre = ag_ctx.funcionAgregacion().getText().lower()
            ids = ag_ctx.ID()
            antes = ag_ctx.getText().split(")", 1)[0]
            col_ag = ids[0].getText() if "(" in antes and antes.split("(", 1)[1] else None
            alias_ag = ids[-1].getText() if ag_ctx.COMO() else (
                f"{fn_nombre}_{col_ag}" if col_ag else "cantidad")
            if not col_ag and fn_nombre not in ("contar", "conteo"):
                raise ErrorSemantico(f"{fn_nombre} requiere una columna", ag_ctx.start.line, ag_ctx.start.column)

            if col_ag:
                self.verificar_columna(nombre_pocion, col_ag, linea=ag_ctx.start.line, columna=ag_ctx.start.column)

            lista_agregaciones.append({
                "funcion": fn_nombre,
                "columna": col_ag,
                "alias": alias_ag
            })

        resultado = MotorDatos.destilar(pocion_origen, cols_grupo, lista_agregaciones)
        print(f"[Hechizo Destilación]: Resumen generado agrupando por {cols_grupo} ({len(resultado)} filas resultantes)")
        return resultado

    def visitDescribirExpr(self, ctx: ArcanumParser.DescribirExprContext):
        # Devuelve la tabla con el resumen estadístico de las columnas numéricas
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        return MotorDatos.describir(pocion)

    def visitInstruccionDescribir(self, ctx: ArcanumParser.InstruccionDescribirContext):
        # Imprime en la consola el resumen estadístico con promedio, desviación, etc
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        print()
        print(f"[ESTADÍSTICAS DESCRIPTIVAS DE '{nombre_pocion}']")
        resumen = MotorDatos.describir(pocion)
        resumen.mostrar()
        print()
        return None

    def visitInstruccionRevelar(self, ctx: ArcanumParser.InstruccionRevelarContext):
        # Muestra en la terminal el contenido de una variable (Poción, escalar, lista, modelo)
        nombre_var = ctx.expresion().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        val = self.visit(ctx.expresion())
        if isinstance(val, Pocion):
            print()
            print(f"[REVELACIÓN DE LA POCIÓN '{nombre_var}']")
            print(f"Dimensiones: {len(val)} registros x {len(val.columnas)} ingredientes")
            print(f"Ingredientes: {val.columnas}")
            print()
            val.mostrar()
            print()
        else:
            print(f"[REVELACIÓN]: {nombre_var} = {val}")
        return None

    def visitInstruccionPreservar(self, ctx: ArcanumParser.InstruccionPreservarContext):
        # Guarda la poción en un archivo CSV en disco
        nombre_pocion = ctx.ID().getText()
        ruta_salida = ctx.CADENA().getText().strip('"')
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        MotorDatos.guardar_csv(pocion, ruta_salida, linea=linea, columna=columna)
        print(f"[Hechizo Preservación]: Poción '{nombre_pocion}' exportada a '{ruta_salida}' ({len(pocion)} filas)")
        return None

    def visitInstruccionForjar(self, ctx: ArcanumParser.InstruccionForjarContext):
        # Genera representaciones visuales (barras, líneas, dispersión, histograma) y las exporta a PNG
        tipo_artefacto = ctx.ID(0).getText()
        origen = ctx.ID(1).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.obtener_pocion(origen, linea=linea, columna=columna)

        eje_x = None
        eje_y = None
        titulo = None
        ruta_salida = None

        if ctx.listaParametros():
            for p_ctx in ctx.listaParametros().parametro():
                if p_ctx.EJE_X():
                    eje_x = p_ctx.ID().getText()
                elif p_ctx.EJE_Y():
                    eje_y = p_ctx.ID().getText()
                elif p_ctx.TITULO():
                    titulo = p_ctx.CADENA().getText().strip('"')
                elif p_ctx.SALIDA() or p_ctx.GUARDAR():
                    ruta_salida = p_ctx.CADENA().getText().strip('"')

        if ctx.CADENA():
            ruta_salida = ctx.CADENA().getText().strip('"')

        return MotorDatos.forjar_grafica(
            tipo=tipo_artefacto,
            pocion=pocion,
            eje_x=eje_x,
            eje_y=eje_y,
            titulo=titulo,
            ruta_salida=ruta_salida
        )

