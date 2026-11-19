from __future__ import annotations
from errores import ErrorSemantico
import os
from analizador import analizar_archivo

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


class RetornoReceta(Exception):
    def __init__(self, valor):
        self.valor = valor

class Recetas:
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

        arbol = analizar_archivo(ruta_compendio)
        # Importar un compendio registra sus recetas, sin ejecutar instrucciones sueltas.
        from visitor import ArcanumVisitorEjecutor
        sub_visitor = ArcanumVisitorEjecutor(self.tabla, self.max_iteraciones)
        for hechizo in arbol.hechizo():
            if hechizo.definicionReceta() is None:
                raise ErrorSemantico("Un compendio solo puede contener definiciones de recetas", hechizo.start.line, hechizo.start.column)
            sub_visitor.visit(hechizo)
        self._compendios[nombre_compendio] = sub_visitor._recetas_locales

        print(f"[Compendio Cargado]: Librería propia '{nombre_compendio}' cargada desde '{ruta_compendio}' ({len(sub_visitor._recetas_locales)} recetas disponibles)")
        return None

    def visitDefinicionReceta(self, ctx: ArcanumParser.DefinicionRecetaContext):
        # Guarda la definición de una función para poder usarla más adelante
        nombre = ctx.ID().getText()
        parametros = [id_n.getText() for id_n in ctx.listaIds().ID()] if ctx.listaIds() else []
        hechizos = ctx.hechizo()
        nodo_devolver = None

        receta = RecetaAlquimica(nombre, parametros, hechizos, nodo_devolver)
        self._recetas_locales[nombre] = receta
        return None

    def visitLlamadaFuncion(self, ctx: ArcanumParser.LlamadaFuncionContext):
        # Puente para redirigir la llamada a la receta correspondiente
        return self.visit(ctx.llamadaReceta())

    def visitLlamadaReceta(self, ctx):
        nombre = ".".join(n.getText() for n in ctx.ID())
        args = [self.visit(e) for e in ctx.listaArgumentos().expresion()] if ctx.listaArgumentos() else []
        return self.llamar(nombre, args, ctx.start.line, ctx.start.column)

    def llamar(self, nombre, argumentos, linea=None, columna=None):
        receta = None
        if "." in nombre:
            compendio, funcion = nombre.split(".", 1)
            if compendio not in self._compendios:
                raise ErrorSemantico(f"El compendio '{compendio}' no ha sido cargado", linea, columna)
            receta = self._compendios[compendio].get(funcion)
        else:
            receta = self._recetas_locales.get(nombre)
            if receta is None and nombre.lower() in self._nativas:
                return self._nativas.ejecutar(nombre.lower(), argumentos, self, linea, columna)
            if receta is None:
                for compendio in self._compendios.values():
                    if nombre in compendio:
                        receta = compendio[nombre]
                        break
        if receta is None:
            raise ErrorSemantico(f"La receta o función '{nombre}' no ha sido definida", linea, columna)
        if len(argumentos) != len(receta.parametros):
            raise ErrorSemantico(f"La receta '{nombre}' espera {len(receta.parametros)} argumentos, pero recibió {len(argumentos)}", linea, columna)
        self._marcos_locales.append(dict(zip(receta.parametros, argumentos)))
        anteriores = self._recetas_locales
        # Las llamadas entre recetas del mismo compendio conservan su contexto.
        if "." in nombre:
            self._recetas_locales = self._compendios[nombre.split(".", 1)[0]]
        try:
            for hechizo in receta.lista_hechizos:
                self.visit(hechizo)
            return None
        except RetornoReceta as retorno:
            return retorno.valor
        finally:
            self._recetas_locales = anteriores
            self._marcos_locales.pop()

    def visitInstruccionDevolver(self, ctx):
        if not self._marcos_locales:
            raise ErrorSemantico("devolver solo se puede usar dentro de una receta", ctx.start.line, ctx.start.column)
        raise RetornoReceta(self.visit(ctx.expresion()))
