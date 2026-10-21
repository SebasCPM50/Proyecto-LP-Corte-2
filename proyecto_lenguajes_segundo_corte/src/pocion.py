"""
Módulo de Estructura de Datos Tabular Propia — Arcanum
Implementación 100% DESDE CERO de una tabla de datos (Poción)
NO UTILIZA PANDAS, NUMPY NI NINGUNA LIBRERÍA EXTERNA

Estructura interna:
  self.columnas: Lista de nombres de columnas ['col1', 'col2']
  self.filas: Lista de diccionarios [{'col1': val1, 'col2': val2}]

Principio de Inmutabilidad Alquímica:
  Cada operación produce una Poción NUEVA, preservando intactos los datos originales
"""

import os
from errores import ErrorSemantico


def _convertir_tipo_dato(texto):
    """
    Convierte una cadena de texto cruda del CSV al tipo de dato nativo correspondiente:
    entero, flotante, booleano, nulo o texto limpio
    """
    texto = texto.strip()
    if texto == "" or texto.upper() in ["NAN", "NULL", "NONE"]:
        return None
    if texto.lower() in ["verdadero", "true"]:
        return True
    if texto.lower() in ["falso", "false"]:
        return False
    # Intentamos convertir a entero
    try:
        return int(texto)
    except ValueError:
        pass
    # Intentamos convertir a flotante
    try:
        return float(texto)
    except ValueError:
        pass
    # Si no es número ni booleano, queda como texto sin comillas externas
    if (texto.startswith('"') and texto.endswith('"')) or (texto.startswith("'") and texto.endswith("'")):
        return texto[1:-1]
    return texto


class Pocion:
    """
    Representa una tabla de datos completa creada desde cero
    Equivalente artesanal a un DataFrame
    """

    def __init__(self, columnas, filas):
        self.columnas = [str(c).strip() for c in columnas]
        # Guardamos copias independientes de cada fila (diccionario)
        self.filas = [dict(f) for f in filas]

    def __len__(self):
        # Retorna la cantidad de registros de la poción
        return len(self.filas)

    def __repr__(self):
        return f"<Pocion: {len(self.filas)} registros x {len(self.columnas)} ingredientes>"

    @classmethod
    def resolver_ruta(cls, ruta):
        # Resuelve la ubicación de un archivo en carpetas conocidas
        if os.path.exists(ruta):
            return ruta
        nombre_archivo = os.path.basename(ruta)
        posibles = [
            os.path.join("csv", nombre_archivo),
            os.path.join("datos", nombre_archivo),
            os.path.join("..", "csv", nombre_archivo),
            os.path.join("..", "datos", nombre_archivo),
            os.path.join("..", ruta)
        ]
        for p in posibles:
            if os.path.exists(p):
                return p
        return ruta

    @classmethod
    def desde_csv(cls, ruta, linea=None, columna=None):
        """
        Lee y parsea un archivo CSV desde cero usando únicamente las funciones
        básicas de lectura de archivos de Python (open, split, strip)
        """
        ruta_resuelta = cls.resolver_ruta(ruta)
        if not os.path.exists(ruta_resuelta):
            raise ErrorSemantico(
                f"No se pudo invocar el archivo: no existe '{ruta}'. "
                f"Verifica la ruta en disco o en la carpeta 'csv/'",
                linea, columna
            )

        try:
            with open(ruta_resuelta, mode="r", encoding="utf-8") as f:
                lineas = [l.strip() for l in f.readlines() if l.strip()]

            if not lineas:
                return cls([], [])

            # Cabecera (nombres de columnas)
            cabecera = [col.strip().strip('"') for col in lineas[0].split(",")]

            # Filas de datos
            filas = []
            for num_linea, linea_texto in enumerate(lineas[1:], start=2):
                partes = linea_texto.split(",")
                # Si hay columnas faltantes al final por comas omitidas, rellenamos con None
                while len(partes) < len(cabecera):
                    partes.append("")

                fila_dict = {}
                for idx, nombre_col in enumerate(cabecera):
                    valor_crudo = partes[idx] if idx < len(partes) else ""
                    fila_dict[nombre_col] = _convertir_tipo_dato(valor_crudo)
                filas.append(fila_dict)

            return cls(cabecera, filas)

        except Exception as e:
            raise ErrorSemantico(f"Error al leer el archivo CSV '{ruta}': {str(e)}", linea, columna)

    def a_csv(self, ruta, linea=None, columna=None):
        """
        Exporta la poción a un archivo CSV en disco sin librerías externas
        Crea carpetas si no existen
        """
        try:
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta, mode="w", encoding="utf-8") as f:
                f.write(",".join(self.columnas) + "\n")
                for fila in self.filas:
                    valores = []
                    for col in self.columnas:
                        v = fila.get(col)
                        if v is None:
                            valores.append("")
                        else:
                            valores.append(str(v))
                    f.write(",".join(valores) + "\n")
            return ruta
        except Exception as e:
            raise ErrorSemantico(f"No se pudo preservar la poción en '{ruta}': {str(e)}", linea, columna)

    def recolectar(self, lista_columnas):
        """
        Selecciona un subconjunto de columnas
        Retorna una nueva Pocion independiente
        """
        nuevas_filas = []
        for fila in self.filas:
            nueva_fila = {c: fila.get(c) for c in lista_columnas}
            nuevas_filas.append(nueva_fila)
        return Pocion(lista_columnas, nuevas_filas)

    def purificar(self, evaluador_condicion):
        """
        Filtra las filas según una función evaluadora
        Retorna una nueva Poción con las filas que cumplan la condición
        """
        nuevas_filas = [f.copy() for f in self.filas if evaluador_condicion(f)]
        return Pocion(self.columnas, nuevas_filas)

    def ordenar(self, columna, ascendente=True):
        """
        Ordena las filas según el valor de una columna
        Maneja valores nulos de forma segura colocándolos al final
        """
        def clave_orden(fila):
            v = fila.get(columna)
            if v is None:
                return (1, 0)
            return (0, v)

        filas_ordenadas = sorted(self.filas, key=clave_orden, reverse=not ascendente)
        return Pocion(self.columnas, filas_ordenadas)

    def transmutar(self, nombre_columna, evaluador_expresion):
        """
        Calcula una nueva columna para cada fila evaluando una fórmula
        Retorna una nueva Poción con la columna agregada
        """
        nuevas_cols = list(self.columnas)
        if nombre_columna not in nuevas_cols:
            nuevas_cols.append(nombre_columna)

        nuevas_filas = []
        for fila in self.filas:
            copia = fila.copy()
            copia[nombre_columna] = evaluador_expresion(fila)
            nuevas_filas.append(copia)
        return Pocion(nuevas_cols, nuevas_filas)

    def sanar_descartar_nulos(self):
        # Elimina cualquier fila que contenga al menos un valor nulo
        filas_limpias = []
        for fila in self.filas:
            tiene_nulo = any(fila.get(c) is None for c in self.columnas)
            if not tiene_nulo:
                filas_limpias.append(fila.copy())
        return Pocion(self.columnas, filas_limpias)

    def sanar_llenar_nulos(self, columna, valor_relleno):
        # Rellena los valores nulos de una columna específica con el valor dado
        nuevas_filas = []
        for fila in self.filas:
            copia = fila.copy()
            if copia.get(columna) is None:
                copia[columna] = valor_relleno
            nuevas_filas.append(copia)
        return Pocion(self.columnas, nuevas_filas)

    def destilar(self, columnas_grupo, lista_agregaciones):
        """
        Agrupa las filas por una o más columnas y calcula agregaciones estadísticas
        Implementado completamente con diccionarios y matemáticas nativas
        """
        grupos = {}
        for fila in self.filas:
            clave = tuple(fila.get(col) for col in columnas_grupo)
            if clave not in grupos:
                grupos[clave] = []
            grupos[clave].append(fila)

        columnas_resumen = list(columnas_grupo)
        for ag in lista_agregaciones:
            alias = ag["alias"]
            if alias not in columnas_resumen:
                columnas_resumen.append(alias)

        filas_resumen = []
        for clave, filas_del_grupo in grupos.items():
            fila_nueva = {}
            for idx, col in enumerate(columnas_grupo):
                fila_nueva[col] = clave[idx]

            for ag in lista_agregaciones:
                fn = ag["funcion"].lower()
                col_obj = ag.get("columna")
                alias = ag["alias"]

                if col_obj:
                    valores = [f[col_obj] for f in filas_del_grupo if f.get(col_obj) is not None and isinstance(f.get(col_obj), (int, float))]
                else:
                    valores = []

                n = len(valores)
                conteo_filas = len(filas_del_grupo)

                if fn in ["contar", "conteo"]:
                    resultado = conteo_filas
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
        Calcula un resumen estadístico para todas las columnas numéricas de la poción
        Retorna una nueva Poción resumen
        """
        metricas = ["conteo", "media", "desviacion", "minimo", "maximo"]
        columnas_numericas = []

        for col in self.columnas:
            valores_num = [f[col] for f in self.filas if f.get(col) is not None and isinstance(f.get(col), (int, float))]
            if len(valores_num) > 0:
                columnas_numericas.append(col)

        columnas_resumen = ["metrica"] + columnas_numericas
        filas_resumen = []

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
        Imprime la tabla completa sin omitir ningún registro
        Formato limpio de columnas alineadas sin líneas pesadas de separación
        """
        if not self.filas:
            print("  (Poción vacía: 0 registros)")
            return

        # Calculamos el ancho de cada columna para alinear bien
        anchos = {}
        for col in self.columnas:
            max_len = len(col)
            for f in self.filas:
                v = f.get(col)
                # Mostramos 'None' explícitamente para que no se pierdan datos nulos
                v_str = "None" if v is None else str(v)
                if len(v_str) > max_len:
                    max_len = len(v_str)
            anchos[col] = max_len + 3

        # Imprimimos encabezado
        cabecera = "".join([col.ljust(anchos[col]) for col in self.columnas])
        print(cabecera)

        # Imprimimos TODAS las filas
        for f in self.filas:
            fila_txt = ""
            for col in self.columnas:
                v = f.get(col)
                v_str = "None" if v is None else str(v)
                fila_txt += v_str.ljust(anchos[col])
            print(fila_txt)
