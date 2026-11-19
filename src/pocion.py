"""
Estructura de datos artesanal para Arcanum
Acá creamos nuestra propia tabla de datos (Poción) desde cero
No usamos Pandas ni NumPy ni ninguna librería externa, solo listas y diccionarios nativos de Python

Cómo se guardan las cosas por dentro:
  self.columnas: Lista con los nombres de las columnas ['fecha', 'precio']
  self.filas: Lista de diccionarios [{'fecha': '2026-01-05', 'precio': 150000}]

Regla importante:
  Cada vez que modificamos algo, devolvemos una Poción nueva para no dañar los datos originales
"""

import os
import json
from errores import ErrorSemantico


from datos_io import ArchivosPocion, _convertir_tipo_dato
from aleatorio import numero_aleatorio, _generar_siguiente_azar


class Pocion(ArchivosPocion):
    """
    Esta es nuestra clase de tabla de datos hecha a mano
    Vendría siendo como nuestro propio DataFrame pero sin usar librerías externas
    """

    def __init__(self, columnas, filas):
        # Guardamos la lista de nombres de columnas bien limpias
        self.columnas = [str(c).strip() for c in columnas]
        # Guardamos copias independientes de cada fila en diccionarios para no cruzarlas
        self.filas = [dict(f) for f in filas]

    def __len__(self):
        # Nos dice cuántas filas tiene la tabla
        return len(self.filas)

    def __repr__(self):
        # Mensaje corto para ver cuántas filas e ingredientes tiene la poción
        return f"<Pocion: {len(self.filas)} registros x {len(self.columnas)} ingredientes>"

    def recolectar(self, lista_columnas):
        """
        Selecciona solo las columnas que le pedimos y descarta las demás
        Devuelve una Poción nueva con únicamente esas columnas
        """
        nuevas_filas = []
        for fila in self.filas:
            # Armamos una fila nueva solo con las claves solicitadas
            nueva_fila = {c: fila.get(c) for c in lista_columnas}
            nuevas_filas.append(nueva_fila)
        return Pocion(lista_columnas, nuevas_filas)

    def purificar(self, evaluador_condicion):
        """
        Filtra las filas pasando una función que dice True si la fila se queda
        Devuelve una Poción nueva solo con los datos que pasaron la prueba
        """
        nuevas_filas = [f.copy() for f in self.filas if evaluador_condicion(f)]
        return Pocion(self.columnas, nuevas_filas)

    def ordenar(self, columna, ascendente=True):
        """
        Ordena todas las filas según el valor de una columna
        Si hay valores nulos None, los manda al final para que no rompan la comparación
        """
        presentes = [f for f in self.filas if f.get(columna) is not None]
        ausentes = [f for f in self.filas if f.get(columna) is None]
        filas_ordenadas = sorted(presentes, key=lambda f: f[columna], reverse=not ascendente) + ausentes
        return Pocion(self.columnas, filas_ordenadas)

    def transmutar(self, nombre_columna, evaluador_expresion):
        """
        Crea una columna nueva calculando su valor fila por fila con una fórmula
        Devuelve una Poción nueva con la columna adicional
        """
        # Copiamos la lista de columnas y agregamos la nueva si no estaba
        nuevas_cols = list(self.columnas)
        if nombre_columna not in nuevas_cols:
            nuevas_cols.append(nombre_columna)

        # Calculamos el nuevo valor para cada fila y lo guardamos en su diccionario
        nuevas_filas = []
        for fila in self.filas:
            copia = fila.copy()
            copia[nombre_columna] = evaluador_expresion(fila)
            nuevas_filas.append(copia)
        return Pocion(nuevas_cols, nuevas_filas)

    def sanar_descartar_nulos(self):
        """
        Quita cualquier fila que tenga al menos una celda vacía o None
        Nos deja la tabla 100% limpia sin registros incompletos
        """
        filas_limpias = []
        for fila in self.filas:
            # Revisamos si alguna columna de esta fila tiene valor None
            tiene_nulo = any(fila.get(c) is None for c in self.columnas)
            if not tiene_nulo:
                filas_limpias.append(fila.copy())
        return Pocion(self.columnas, filas_limpias)

    def sanar_llenar_nulos(self, columna, valor_relleno):
        """
        Busca las celdas nulas en una columna y les pone un valor por defecto
        Por ejemplo si la nota es None le pone 0
        """
        nuevas_filas = []
        for fila in self.filas:
            copia = fila.copy()
            if copia.get(columna) is None:
                copia[columna] = valor_relleno
            nuevas_filas.append(copia)
        return Pocion(self.columnas, nuevas_filas)

    def destilar(self, columnas_grupo, lista_agregaciones):
        """
        Agrupa las filas por una o más categorías y saca cálculos matemáticos
        como suma, promedio, mediana, mínimo, máximo o conteo
        Hecho todo a pulso con diccionarios y matemáticas básicas
        """
        # Primero agrupamos las filas en un diccionario usando como clave los valores de las columnas agrupadoras
        grupos = {}
        for fila in self.filas:
            clave = tuple(fila.get(col) for col in columnas_grupo)
            if clave not in grupos:
                grupos[clave] = []
            grupos[clave].append(fila)

        # Preparamos las columnas que va a tener la tabla final de resumen
        columnas_resumen = list(columnas_grupo)
        for ag in lista_agregaciones:
            alias = ag["alias"]
            if alias not in columnas_resumen:
                columnas_resumen.append(alias)

        # Ahora calculamos las operaciones matemáticas para cada grupo
        filas_resumen = []
        for clave, filas_del_grupo in grupos.items():
            fila_nueva = {}
            for idx, col in enumerate(columnas_grupo):
                fila_nueva[col] = clave[idx]

            for ag in lista_agregaciones:
                fn = ag["funcion"].lower()
                col_obj = ag.get("columna")
                alias = ag["alias"]

                # Extraemos solo los valores numéricos válidos del grupo
                if col_obj:
                    valores = [f[col_obj] for f in filas_del_grupo if f.get(col_obj) is not None and isinstance(f.get(col_obj), (int, float))]
                else:
                    valores = []

                n = len(valores)
                conteo_filas = len(filas_del_grupo)

                # Acá evaluamos qué operación matemática nos pidieron
                if fn in ["contar", "conteo"]:
                    resultado = conteo_filas if col_obj is None else sum(f.get(col_obj) is not None for f in filas_del_grupo)
                elif fn == "suma":
                    resultado = sum(valores) if valores else 0
                elif fn in ["media", "promedio"]:
                    resultado = (sum(valores) / n) if n > 0 else 0.0
                elif fn == "mediana":
                    if not valores:
                        resultado = 0.0
                    else:
                        ordenados = sorted(valores)
                        mitad = n // 2
                        if n % 2 == 1:
                            resultado = ordenados[mitad]
                        else:
                            resultado = (ordenados[mitad - 1] + ordenados[mitad]) / 2.0
                elif fn in ["minimo", "min"]:
                    resultado = min(valores) if valores else 0
                elif fn in ["maximo", "max"]:
                    resultado = max(valores) if valores else 0
                elif fn in ["desviacion", "std"]:
                    if n <= 1:
                        resultado = 0.0
                    else:
                        prom = sum(valores) / n
                        varianza = sum((x - prom) ** 2 for x in valores) / (n - 1)
                        resultado = varianza ** 0.5
                else:
                    resultado = None

                fila_nueva[alias] = resultado

            filas_resumen.append(fila_nueva)

        return Pocion(columnas_resumen, filas_resumen)

    def describir(self):
        """
        Saca un resumen estadístico rápido de todas las columnas numéricas
        Muestra conteo, promedio, desviación, mínimo y máximo
        """
        metricas = ["conteo", "media", "desviacion", "minimo", "maximo"]
        columnas_numericas = []

        # Detectamos cuáles columnas son números
        for col in self.columnas:
            valores_num = [f[col] for f in self.filas if f.get(col) is not None and isinstance(f.get(col), (int, float))]
            if len(valores_num) > 0:
                columnas_numericas.append(col)

        columnas_resumen = ["metrica"] + columnas_numericas
        filas_resumen = []

        # Calculamos cada una de las 5 métricas para cada columna numérica
        for m in metricas:
            fila_m = {"metrica": m}
            for col in columnas_numericas:
                vals = [f[col] for f in self.filas if f.get(col) is not None and isinstance(f.get(col), (int, float))]
                n = len(vals)
                if m == "conteo":
                    fila_m[col] = n
                elif m == "media":
                    fila_m[col] = round(sum(vals) / n, 2) if n > 0 else 0.0
                elif m == "desviacion":
                    if n <= 1:
                        fila_m[col] = 0.0
                    else:
                        p = sum(vals) / n
                        v = sum((x - p) ** 2 for x in vals) / (n - 1)
                        fila_m[col] = round(v ** 0.5, 2)
                elif m == "minimo":
                    fila_m[col] = min(vals) if vals else 0
                elif m == "maximo":
                    fila_m[col] = max(vals) if vals else 0
            filas_resumen.append(fila_m)

        return Pocion(columnas_resumen, filas_resumen)

    def mostrar(self):
        """
        Imprime la tabla completa en pantalla sin recortar filas
        Alinea los textos de cada columna y muestra explícitamente None si hay celdas vacías
        """
        if not self.filas:
            print("  (Poción vacía: 0 registros)")
            return

        # Calculamos el tamaño más largo de cada columna para que quede bien alineado
        anchos = {}
        for col in self.columnas:
            max_len = len(col)
            for f in self.filas:
                v = f.get(col)
                v_str = "None" if v is None else str(v)
                if len(v_str) > max_len:
                    max_len = len(v_str)
            anchos[col] = max_len + 3

        # Imprimimos la cabecera con los nombres de las columnas
        cabecera = "".join([col.ljust(anchos[col]) for col in self.columnas])
        print(cabecera)

        # Imprimimos todas y cada una de las filas sin omitir ninguna
        for f in self.filas:
            fila_txt = ""
            for col in self.columnas:
                v = f.get(col)
                v_str = "None" if v is None else str(v)
                fila_txt += v_str.ljust(anchos[col])
            print(fila_txt)

    def muestra_aleatoria(self, cantidad):
        """
        Saca una muestra al azar de varias filas de la tabla sin repetir
        Sirve por si queremos analizar solo un pedazo aleatorio de los datos
        """
        if cantidad >= len(self.filas):
            return Pocion(self.columnas, [f.copy() for f in self.filas])

        # Mezclamos los índices con el algoritmo de Fisher-Yates hecho a mano sin librerías
        indices = list(range(len(self.filas)))
        for i in range(len(indices) - 1, 0, -1):
            j = _generar_siguiente_azar() % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]

        filas_muestra = [self.filas[idx].copy() for idx in indices[:cantidad]]
        return Pocion(self.columnas, filas_muestra)

    def a_matriz(self, columnas=None):
        """
        Puente de interoperabilidad: convierte columnas numéricas de la Poción a Matriz
        (conecta nuestro DataFrame artesanal con nuestra versión artesanal de NumPy).
        """
        from estructuras.matriz import Matriz
        cols = columnas if columnas is not None else [
            c for c in self.columnas
            if any(isinstance(f.get(c), (int, float)) for f in self.filas)
        ]
        return Matriz.desde_pocion(self, cols)

