"""
Intérprete semántico con el patrón Visitor para Arcanum
Acá recorremos el árbol de análisis sintáctico que generó ANTLR
y ejecutamos cada instrucción una por una usando nuestra clase artesanal Pocion
No usamos Pandas ni NumPy ni import de Python para compendios
"""

import os
import sys

# Agregamos la carpeta generated para poder usar el visitor generado por ANTLR
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
    Representa una función propia creada dentro del lenguaje Arcanum
    Guarda el nombre, los nombres de los parámetros, las instrucciones y lo que devuelve
    """
    def __init__(self, nombre, parametros, lista_hechizos, nodo_devolver):
        # Nombre de la receta por ejemplo 'calcular_iva'
        self.nombre = nombre
        # Lista con los nombres de las variables que recibe como entrada
        self.parametros = parametros
        # Lista de instrucciones que se ejecutan cuando la llamemos
        self.lista_hechizos = lista_hechizos
        # Expresión que retorna al final con devolver
        self.nodo_devolver = nodo_devolver


class ArcanumVisitorEjecutor(ArcanumVisitor):
    """
    Clase principal que recorre los nodos del árbol y va ejecutando el código de Arcanum
    """

    def __init__(self, tabla_simbolos=None):
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
        self.tabla.verificar_columnas(nombre_pocion, columnas, linea=linea, columna=columna)
        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        resultado = MotorDatos.recolectar(pocion_origen, columnas)
        print(f"[Hechizo Recolección]: Se seleccionaron {columnas} de '{nombre_pocion}'")
        return resultado

    def visitPurificarExpr(self, ctx: ArcanumParser.PurificarExprContext):
        # Filtra las filas evaluando la condición para cada registro de la tabla
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

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
        # Agrega una columna calculando una fórmula matemática fila por fila
        nombre_pocion = ctx.ID(0).getText()
        columna_nueva = ctx.ID(1).getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

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
        # Agrupa filas por categorías y calcula métricas como promedios o sumas
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        cols_grupo = [id_node.getText() for id_node in ctx.listaIds().ID()]
        self.tabla.verificar_columnas(nombre_pocion, cols_grupo, linea=linea, columna=columna)
        pocion_origen = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)

        # Extraemos la lista de funciones que nos pidieron calcular
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
        # Devuelve la tabla con el resumen estadístico de las columnas numéricas
        nombre_pocion = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        return MotorDatos.describir(pocion)

    def visitInstruccionDescribir(self, ctx: ArcanumParser.InstruccionDescribirContext):
        # Imprime en la consola el resumen estadístico con promedio, desviación, etc
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
        # Muestra en la terminal toda la tabla completa sin cortar filas
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
        # Guarda la poción en un archivo CSV en disco
        nombre_pocion = ctx.ID().getText()
        ruta_salida = ctx.CADENA().getText().strip('"')
        linea = ctx.start.line
        columna = ctx.start.column

        pocion = self.tabla.obtener_pocion(nombre_pocion, linea=linea, columna=columna)
        MotorDatos.guardar_csv(pocion, ruta_salida, linea=linea, columna=columna)
        print(f"[Hechizo Preservación]: Poción '{nombre_pocion}' exportada a '{ruta_salida}' ({len(pocion)} filas)")
        return None

    def visitInstruccionForjar(self, ctx: ArcanumParser.InstruccionForjarContext):
        # Reconoce la instrucción de visualización gráfica (reservada para el tercer corte)
        tipo_artefacto = ctx.ID(0).getText()
        origen = ctx.ID(1).getText()
        print(f"[Hechizo de Forja reconocido]: Se preparará artefacto visual '{tipo_artefacto}' desde '{origen}' (reservado para Corte 3)")
        return None

    # Compendios y recetas (librerías propias)

    def visitInstruccionUsar(self, ctx: ArcanumParser.InstruccionUsarContext):
        # Carga un compendio externo escrito en Arcanum y guarda sus recetas disponibles
        nombre_compendio = ctx.ID().getText()
        linea = ctx.start.line
        columna = ctx.start.column

        # Buscamos el archivo del compendio en la carpeta compendios/
        ruta_compendio = os.path.join("compendios", f"{nombre_compendio}.arc")
        if not os.path.exists(ruta_compendio):
            ruta_compendio = os.path.join(os.path.dirname(__file__), "..", "compendios", f"{nombre_compendio}.arc")
        
        if not os.path.exists(ruta_compendio):
            raise ErrorSemantico(
                f"No se encontró el compendio '{nombre_compendio}' en 'compendios/{nombre_compendio}.arc'",
                linea, columna
            )

        # Parseamos el archivo del compendio con ANTLR de forma limpia
        entrada = FileStream(ruta_compendio, encoding="utf-8")
        lexer = ArcanumLexer(entrada)
        tokens = CommonTokenStream(lexer)
        parser = ArcanumParser(tokens)
        arbol = parser.programa()

        # Usamos un visitor auxiliar para registrar las recetas del compendio
        sub_visitor = ArcanumVisitorEjecutor(self.tabla)
        sub_visitor.visit(arbol)
        self._compendios[nombre_compendio] = sub_visitor._recetas_locales

        print(f"[Compendio Cargado]: Librería propia '{nombre_compendio}' cargada desde '{ruta_compendio}' ({len(sub_visitor._recetas_locales)} recetas disponibles)")
        return None

    def visitDefinicionReceta(self, ctx: ArcanumParser.DefinicionRecetaContext):
        # Guarda la definición de una función para poder usarla más adelante
        nombre = ctx.ID().getText()
        parametros = [id_n.getText() for id_n in ctx.listaIds().ID()] if ctx.listaIds() else []
        hechizos = ctx.hechizo()
        nodo_devolver = ctx.instruccionDevolver()

        receta = RecetaAlquimica(nombre, parametros, hechizos, nodo_devolver)
        self._recetas_locales[nombre] = receta
        return None

    def visitLlamadaFuncion(self, ctx: ArcanumParser.LlamadaFuncionContext):
        # Puente para redirigir la llamada a la receta correspondiente
        return self.visit(ctx.llamadaReceta())

    def visitLlamadaReceta(self, ctx: ArcanumParser.LlamadaRecetaContext):
        # Ejecuta una receta pasándole sus argumentos y manejando su propio marco de memoria
        ids = ctx.ID()
        linea = ctx.start.line
        columna = ctx.start.column

        # Revisamos si la llamaron con prefijo de compendio como 'matematicas.calcular_iva'
        if len(ids) == 2:
            compendio_nom = ids[0].getText()
            receta_nom = ids[1].getText()
            if compendio_nom not in self._compendios:
                raise ErrorSemantico(f"El compendio '{compendio_nom}' no ha sido cargado con 'usar compendio {compendio_nom};'", linea, columna)
            if receta_nom not in self._compendios[compendio_nom]:
                raise ErrorSemantico(f"La receta '{receta_nom}' no existe en el compendio '{compendio_nom}'", linea, columna)
            receta = self._compendios[compendio_nom][receta_nom]
        else:
            # O si la llamaron directo por su nombre
            receta_nom = ids[0].getText()
            if receta_nom in self._recetas_locales:
                receta = self._recetas_locales[receta_nom]
            else:
                encontrada = None
                for c_nom, c_dict in self._compendios.items():
                    if receta_nom in c_dict:
                        encontrada = c_dict[receta_nom]
                        break
                if encontrada:
                    receta = encontrada
                elif receta_nom.lower() in ["random", "aleatorio", "azar"]:
                    # Acá resolvemos la función random nativa del lenguaje hecha a mano
                    argumentos = []
                    if ctx.listaArgumentos():
                        for expr_arg in ctx.listaArgumentos().expresion():
                            argumentos.append(self.visit(expr_arg))
                    from pocion import numero_aleatorio
                    if len(argumentos) == 0:
                        return numero_aleatorio()
                    elif len(argumentos) == 1:
                        return numero_aleatorio(0, argumentos[0])
                    elif len(argumentos) == 2:
                        return numero_aleatorio(argumentos[0], argumentos[1])
                    else:
                        raise ErrorSemantico("La función random espera máximo 2 argumentos (minimo, maximo)", linea, columna)
                else:
                    raise ErrorSemantico(f"La receta o función '{receta_nom}' no ha sido definida", linea, columna)


        # Evaluamos cada uno de los argumentos que nos pasaron
        argumentos = []
        if ctx.listaArgumentos():
            for expr_arg in ctx.listaArgumentos().expresion():
                argumentos.append(self.visit(expr_arg))

        # Comprobamos que pasaron exactamente la cantidad de parámetros requeridos
        if len(argumentos) != len(receta.parametros):
            raise ErrorSemantico(
                f"La receta '{receta.nombre}' espera {len(receta.parametros)} ingredientes (argumentos), pero recibió {len(argumentos)}",
                linea, columna
            )

        # Creamos el marco de memoria local para no sobreescribir variables globales
        marco_local = dict(zip(receta.parametros, argumentos))
        self._marcos_locales.append(marco_local)

        try:
            # Ejecutamos las instrucciones de la receta
            for h in receta.lista_hechizos:
                self.visit(h)
            # Si tiene cláusula devolver, evaluamos y retornamos el resultado
            if receta.nodo_devolver:
                return self.visit(receta.nodo_devolver.expresion())
            return None
        finally:
            # Al terminar la función sacamos su memoria de la pila
            self._marcos_locales.pop()

    # Condiciones y comparaciones lógicas

    def visitCondicionY(self, ctx: ArcanumParser.CondicionYContext):
        # Operador lógico Y (ambas condiciones deben ser verdaderas)
        izq = self.visit(ctx.condicion(0))
        der = self.visit(ctx.condicion(1))
        return bool(izq and der)

    def visitCondicionO(self, ctx: ArcanumParser.CondicionOContext):
        # Operador lógico O (con que una sea verdadera ya pasa)
        izq = self.visit(ctx.condicion(0))
        der = self.visit(ctx.condicion(1))
        return bool(izq or der)

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

        # 1. Si estamos dentro de una receta y existe como parámetro o variable local
        if self._marcos_locales and nombre in self._marcos_locales[-1]:
            return self._marcos_locales[-1][nombre]

        # 2. Si estamos dentro de un filtro o columna calculada y coincide con una columna de la fila activa
        if self._fila_activa is not None and nombre in self._fila_activa:
            return self._fila_activa[nombre]

        # 3. Si existe en la tabla de símbolos global
        if self.tabla.existe(nombre):
            return self.tabla.obtener_valor(nombre, linea, columna)

        # Si no la encontró en ningún lado avisamos qué columnas sí existen para orientar al usuario
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
