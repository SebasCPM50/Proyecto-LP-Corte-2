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
from errores import ErrorSemantico


def _convertir_tipo_dato(texto):
    """
    Toma el texto que viene de una celda del CSV y descubre qué tipo de dato es
    para convertirlo a entero, flotante, booleano, nulo o dejarlo en texto limpio
    """
    texto = texto.strip()
    
    # Si la celda está vacía o dice NaN o null, la dejamos como None
    if texto == "" or texto.upper() in ["NAN", "NULL", "NONE"]:
        return None
        
    # Si dice verdadero o true, lo volvemos un booleano True
    if texto.lower() in ["verdadero", "true"]:
        return True
        
    # Si dice falso o false, lo volvemos un booleano False
    if texto.lower() in ["falso", "false"]:
        return False
        
    # Probamos si es un número entero como 10 o 500
    try:
        return int(texto)
    except ValueError:
        pass
        
    # Probamos si es un número decimal como 15.5 o 99.99
    try:
        return float(texto)
    except ValueError:
        pass
        
    # Si tiene comillas a los lados se las quitamos para que quede el texto limpio
    if (texto.startswith('"') and texto.endswith('"')) or (texto.startswith("'") and texto.endswith("'")):
        return texto[1:-1]
        
    return texto


# Semilla inicial para generar números aleatorios sin importar ninguna librería externa
_semilla_azar = (id(object()) * 31 + os.getpid()) & 0x7fffffff


def _generar_siguiente_azar():
    # Algoritmo matemático congruencial para sacar números al azar hecho a mano sin librerías
    global _semilla_azar
    _semilla_azar = (_semilla_azar * 1103515245 + 12345) & 0x7fffffff
    return _semilla_azar


def numero_aleatorio(minimo=0, maximo=1):
    # Genera un número al azar entre un mínimo y un máximo
    # Si no le pasan parámetros devuelve un decimal entre 0 y 1
    azar_crudo = _generar_siguiente_azar() / 2147483647.0
    if minimo == 0 and maximo == 1:
        return round(azar_crudo, 4)
    if isinstance(minimo, int) and isinstance(maximo, int):
        rango = (maximo - minimo) + 1
        return minimo + int(azar_crudo * rango)
    return round(minimo + azar_crudo * (maximo - minimo), 4)



class Pocion:
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

    @classmethod
    def resolver_ruta(cls, ruta):
        # Busca el archivo en la ruta dada o en carpetas comunes como csv/ o datos/
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
        Lee un archivo CSV desde cero usando open() y split() nativos de Python
        No usa el módulo csv de Python ni Pandas
        """
        # Primero buscamos en qué carpeta está el archivo
        ruta_resuelta = cls.resolver_ruta(ruta)
        if not os.path.exists(ruta_resuelta):
            raise ErrorSemantico(
                f"No se pudo invocar el archivo: no existe '{ruta}'. "
                f"Verifica la ruta en disco o en la carpeta 'csv/'",
                linea, columna
            )

        try:
            # Abrimos el archivo en modo lectura con texto UTF-8
            with open(ruta_resuelta, mode="r", encoding="utf-8") as f:
                lineas = [l.strip() for l in f.readlines() if l.strip()]

            # Si el archivo no tiene nada adentro, devolvemos una tabla vacía
            if not lineas:
                return cls([], [])

            # La primera línea siempre tiene los nombres de las columnas
            cabecera = [col.strip().strip('"') for col in lineas[0].split(",")]

            # Ahora recorremos las demás líneas para sacar los datos fila por fila
            filas = []
            for num_linea, linea_texto in enumerate(lineas[1:], start=2):
                partes = linea_texto.split(",")
                # Si una fila tiene menos comas de las necesarias, rellenamos con texto vacío
                while len(partes) < len(cabecera):
                    partes.append("")

                # Armamos el diccionario de esta fila asociando columna con su valor convertido
                fila_dict = {}
                for idx, nombre_col in enumerate(cabecera):
                    valor_crudo = partes[idx] if idx < len(partes) else ""
                    fila_dict[nombre_col] = _convertir_tipo_dato(valor_crudo)
                filas.append(fila_dict)

            # Devolvemos la Poción lista con su cabecera y todas las filas
            return cls(cabecera, filas)

        except Exception as e:
            raise ErrorSemantico(f"Error al leer el archivo CSV '{ruta}': {str(e)}", linea, columna)

    def a_csv(self, ruta, linea=None, columna=None):
        """
        Guarda la poción en un archivo CSV en el disco
        Escribe primero las columnas y luego cada fila separada por comas
        """
        try:
            # Si la carpeta de destino no existe, la creamos de una vez
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta, mode="w", encoding="utf-8") as f:
                # Escribimos los nombres de las columnas separados por coma
                f.write(",".join(self.columnas) + "\n")
                
                # Escribimos cada fila sacando los valores en el mismo orden de las columnas
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
        def clave_orden(fila):
            v = fila.get(columna)
            # Con esto los valores nulos siempre quedan al final
            if v is None:
                return (1, 0)
            return (0, v)

        filas_ordenadas = sorted(self.filas, key=clave_orden, reverse=not ascendente)
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

