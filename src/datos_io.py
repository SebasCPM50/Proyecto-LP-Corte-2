from __future__ import annotations
import os
import json
import csv
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


class ArchivosPocion:
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
        # Búsqueda insensible a mayúsculas/minúsculas para compatibilidad en Linux
        carpetas = [os.path.dirname(ruta) or ".", "datos", "csv", os.path.join("..", "datos"), os.path.join("..", "csv")]
        nombre_lower = nombre_archivo.lower()
        for c in carpetas:
            if os.path.isdir(c):
                for f in os.listdir(c):
                    if f.lower() == nombre_lower:
                        return os.path.join(c, f)
        return ruta

    @classmethod
    def desde_csv(cls, ruta, linea=None, columna=None):
        """
        Lee CSV con el módulo estándar csv, incluyendo comas, comillas y saltos dentro de celdas.
        """
        # Si la ruta termina en .json, delegamos directamente a la lectura JSON
        if ruta.strip().lower().endswith(".json"):
            return cls.desde_json(ruta, linea, columna)

        # Primero buscamos en qué carpeta está el archivo
        ruta_resuelta = cls.resolver_ruta(ruta)
        if not os.path.exists(ruta_resuelta):
            raise ErrorSemantico(
                f"No se pudo invocar el archivo: no existe '{ruta}'. "
                f"Verifica la ruta en disco o en la carpeta 'csv/'",
                linea, columna
            )

        try:
            with open(ruta_resuelta, newline="", encoding="utf-8-sig") as archivo:
                lector = csv.reader(archivo, strict=True)
                cabecera = next(lector, [])
                cabecera = [c.strip() for c in cabecera]
                if any(not c for c in cabecera) or len(set(cabecera)) != len(cabecera):
                    raise ValueError("Las columnas deben tener nombres únicos y no vacíos")
                filas = []
                for partes in lector:
                    if not partes:
                        continue
                    if len(partes) > len(cabecera):
                        raise ValueError(f"Fila {lector.line_num}: sobran valores respecto a la cabecera")
                    partes += [""] * (len(cabecera) - len(partes))
                    filas.append({c: _convertir_tipo_dato(v) for c, v in zip(cabecera, partes)})
            return cls(cabecera, filas)
        except (OSError, ValueError, csv.Error) as error:
            raise ErrorSemantico(f"Error al leer CSV '{ruta}': {error}", linea, columna) from error

    @classmethod
    def desde_json(cls, ruta, linea=None, columna=None):
        """
        Lee un archivo JSON estructurado (lista de diccionarios o formato registros)
        Usa el módulo estándar json de Python sin librerías externas
        """
        ruta_resuelta = cls.resolver_ruta(ruta)
        if not os.path.exists(ruta_resuelta):
            raise ErrorSemantico(
                f"No se pudo invocar el archivo: no existe '{ruta}'. "
                f"Verifica la ruta en disco o en la carpeta 'datos/'",
                linea, columna
            )

        try:
            with open(ruta_resuelta, mode="r", encoding="utf-8") as f:
                datos = json.load(f)

            if isinstance(datos, list):
                if not datos:
                    return cls([], [])
                # Obtenemos las columnas respetando el orden de aparición
                columnas = []
                for elem in datos:
                    if isinstance(elem, dict):
                        for k in elem.keys():
                            if k not in columnas:
                                columnas.append(k)
                filas = []
                for elem in datos:
                    if isinstance(elem, dict):
                        fila_dict = {}
                        for col in columnas:
                            val = elem.get(col)
                            if isinstance(val, str):
                                fila_dict[col] = _convertir_tipo_dato(val)
                            else:
                                fila_dict[col] = val
                        filas.append(fila_dict)
                return cls(columnas, filas)
            elif isinstance(datos, dict):
                columnas = datos.get("columnas", [])
                filas_raw = datos.get("filas", datos.get("datos", []))
                filas = []
                for item in filas_raw:
                    if isinstance(item, dict):
                        filas.append(item)
                    elif isinstance(item, (list, tuple)):
                        filas.append({col: val for col, val in zip(columnas, item)})
                return cls(columnas, filas)
            else:
                raise ErrorSemantico(f"El archivo JSON '{ruta}' debe contener una lista de objetos o registros", linea, columna)

        except Exception as e:
            if isinstance(e, ErrorSemantico):
                raise e
            raise ErrorSemantico(f"Error al leer el archivo JSON '{ruta}': {str(e)}", linea, columna)

    @classmethod
    def desde_excel(cls, ruta, linea=None, columna=None):
        """
        Lee la hoja activa de un archivo .xlsx usando openpyxl.
        """
        ruta_resuelta = cls.resolver_ruta(ruta)
        if not os.path.exists(ruta_resuelta):
            raise ErrorSemantico(
                f"No se pudo invocar el archivo Excel: no existe '{ruta}'. "
                f"Verifica la ruta en disco o en la carpeta 'datos/'",
                linea, columna
            )

        try:
            import openpyxl
            wb = openpyxl.load_workbook(ruta_resuelta, data_only=True, read_only=True)
            try:
                filas_raw = iter(wb.active.iter_rows(values_only=True))
                encabezado = next(filas_raw, ())
                cabecera = [str(c).strip() if c is not None else "" for c in encabezado]
                if any(not c for c in cabecera) or len(set(cabecera)) != len(cabecera):
                    raise ValueError("Excel debe tener encabezados únicos y sin celdas vacías")
                filas = []
                for row in filas_raw:
                    if any(v is not None for v in row):
                        filas.append({col: _convertir_tipo_dato(v) if isinstance(v, str) else v
                                      for col, v in zip(cabecera, row)})
                return cls(cabecera, filas)
            finally:
                wb.close()
        except ImportError as error:
            raise ErrorSemantico("Para leer Excel instala openpyxl con pip install -r requirements.txt", linea, columna) from error
        except Exception as error:
            raise ErrorSemantico(f"Error al leer Excel '{ruta}': {error}", linea, columna) from error

    @classmethod
    def desde_archivo(cls, ruta, linea=None, columna=None):
        """
        Detecta inteligentemente si el archivo es CSV, JSON o Excel (.xlsx) y lo carga en una nueva Poción
        """
        ruta_limpia = ruta.strip().lower()
        if ruta_limpia.endswith(".xls"):
            raise ErrorSemantico("El formato .xls antiguo no está soportado; convierte a .xlsx", linea, columna)
        if ruta_limpia.endswith(".xlsx"):
            return cls.desde_excel(ruta, linea, columna)
        elif ruta_limpia.endswith(".json"):
            return cls.desde_json(ruta, linea, columna)
        return cls.desde_csv(ruta, linea, columna)

    def a_csv(self, ruta, linea=None, columna=None):
        """
        Guarda la poción en un archivo CSV en el disco
        Escribe primero las columnas y luego cada fila separada por comas
        """
        # Si la ruta termina en .json, delegamos directamente a exportar JSON
        if ruta.strip().lower().endswith(".json"):
            return self.a_json(ruta, linea, columna)

        try:
            # Si la carpeta de destino no existe, la creamos de una vez
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(self.columnas)
                for fila in self.filas:
                    escritor.writerow([fila.get(c) for c in self.columnas])
            return ruta
        except Exception as e:
            if isinstance(e, ErrorSemantico):
                raise e
            raise ErrorSemantico(f"No se pudo preservar la poción en '{ruta}': {str(e)}", linea, columna)

    def a_json(self, ruta, linea=None, columna=None):
        """
        Exporta la Poción a un archivo JSON estructurado (lista de diccionarios)
        """
        try:
            directorio = os.path.dirname(ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta, mode="w", encoding="utf-8") as f:
                json.dump(self.filas, f, indent=2, ensure_ascii=False)
            return ruta
        except Exception as e:
            if isinstance(e, ErrorSemantico):
                raise e
            raise ErrorSemantico(f"No se pudo preservar la poción en JSON '{ruta}': {str(e)}", linea, columna)

    def a_archivo(self, ruta, linea=None, columna=None):
        """
        Detecta la extensión del archivo destino y exporta en CSV o JSON
        """
        if ruta.strip().lower().endswith(".json"):
            return self.a_json(ruta, linea, columna)
        if not ruta.strip().lower().endswith(".csv"):
            raise ErrorSemantico("La exportación admite solo .csv o .json", linea, columna)
        return self.a_csv(ruta, linea, columna)

