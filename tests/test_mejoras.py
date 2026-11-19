"""Regresiones de comportamiento comprobadas desde el lenguaje y sus módulos."""
import sys
from pathlib import Path
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / 'src'), str(RAIZ / 'generated')]
from analizador import analizar_texto
from visitor import ArcanumVisitorEjecutor
from errores import ErrorSemantico
from pocion import Pocion


def ejecutar(codigo, limite=10000):
    visitor = ArcanumVisitorEjecutor(max_iteraciones=limite)
    visitor.visit(analizar_texto(codigo))
    return visitor.tabla


@pytest.mark.parametrize('expresion,esperado', [
    ('[10, 20][0] + 2', 12), ('2 * [10, 20][1]', 40),
    ('-2^2', -4), ('(-2)^2', 4), ('2^3^2', 512), ('2^-2', 0.25),
    ('[[1, 2], [3, 4]][1][0]', 3), ('[10, 20][-1]', 20)])
def test_precedencia(expresion, esperado):
    assert ejecutar(f'resultado = {expresion};').obtener_valor('resultado') == esperado


def test_cortocircuito_y_precedencia_logica():
    t = ejecutar('''a = 0; b = 0; c = 0;
      si (falso y 1 / 0 > 2) { a = 1; }
      si (verdadero o desconocida > 0) { b = 1; }
      si (no 1 == 1 y falso o verdadero) { c = 1; }''')
    assert [t.obtener_valor(k) for k in ('a', 'b', 'c')] == [0, 1, 1]
    assert ejecutar('x = 0; si (no verdadero y falso) { x = 1; }').obtener_valor('x') == 0


def test_receta_ambito_y_retorno(capsys):
    t = ejecutar('''x = 99;
      receta procesar(datos) {
        x = 5;
        limpio = purificar datos donde cantidad > 1;
        limpio = transmutar limpio con doble = cantidad * 2;
        mostrar x;
        mostrar limpio;
        si (longitud(limpio) == 1) { devolver limpio; }
        devolver datos;
      }
      entrada = tabla(["cantidad"], [[1], [3]]);
      salida_local = procesar(entrada);''')
    assert t.obtener_valor('x') == 99
    assert t.obtener_pocion('salida_local').filas == [{'cantidad': 3, 'doble': 6}]
    assert '5' in capsys.readouterr().out
    assert not t.existe('limpio')


def test_funcional_y_matrices():
    t = ejecutar('''receta doble(n) { devolver 2*n; }
      receta par(n) { si (n%2 == 0) { devolver verdadero; } devolver falso; }
      receta acum(a,b) { devolver a+b; }
      xs = rango(1, 6); ys = mapear(xs, "doble");
      pares = filtrar(xs, "par"); total = reducir(xs, "acum", 0);
      producto = multiplicar_matrices(matriz([[1,2],[3,4]]), matriz([[2,0],[1,2]]));''')
    assert list(t.obtener_valor('xs')) == [1, 2, 3, 4, 5]
    assert list(t.obtener_valor('ys')) == [2, 4, 6, 8, 10]
    assert list(t.obtener_valor('pares')) == [2, 4]
    assert t.obtener_valor('total') == 15
    assert t.obtener_valor('producto').filas_datos == [[4, 4], [10, 8]]


@pytest.mark.parametrize('codigo', [
    'x = [1, 2][0.5];', 'x = matriz([[1], [2,3]]);',
    'x = rango(1, 5, 0);', 'x = rango(1.5);', 'x = longitud();',
    'devolver 1;', 'x = tabla(["x"], [[1,2]]);', 'x = azar(10, 1);'])
def test_errores_claros(codigo):
    with pytest.raises(ErrorSemantico):
        ejecutar(codigo)


def test_limite_bucle():
    with pytest.raises(ErrorSemantico, match='iteraciones'):
        ejecutar('mientras (verdadero) { x = 1; }', limite=3)


def test_csv_con_comas_comillas_y_saltos(tmp_path):
    original = Pocion(['nombre', 'valor'], [{'nombre': 'Ana, "Luz"\nDiaz', 'valor': 2}])
    ruta = str(tmp_path / 'datos.csv')
    original.a_csv(ruta)
    assert Pocion.desde_csv(ruta).filas == original.filas


def test_conteo_columna_y_nulos_ordenados():
    t = ejecutar('''t = tabla(["grupo", "valor"], [["a", 1], ["a", 2]]);
      r = destilar t por [grupo] agregar contar(valor), contar() como filas;''')
    assert t.obtener_pocion('r').filas[0] == {'grupo': 'a', 'contar_valor': 2, 'filas': 2}
    p = Pocion(['g','v'], [{'g':'a','v':None}, {'g':'a','v':2}, {'g':'a','v':1}])
    assert [f['v'] for f in p.ordenar('v', False).filas] == [2, 1, None]
    assert p.destilar(['g'], [{'funcion':'contar','columna':'v','alias':'n'}]).filas[0]['n'] == 2


def test_compendio_invalido_no_se_ejecuta(tmp_path, monkeypatch):
    (tmp_path / 'compendios').mkdir()
    (tmp_path / 'compendios/roto.arc').write_text('receta f( { devolver 2; }')
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ErrorSemantico, match='sintácticos'):
        ejecutar('usar compendio roto;')


def test_ejercicios_basicos_del_ejemplo7():
    t = ejecutar((RAIZ / 'examples/ejemplo7_casos_profesor.arc').read_text())
    assert t.obtener_valor('fact_5') == 120
    assert t.obtener_valor('fact_10') == 3628800
    assert list(t.obtener_valor('primos')) == [2,3,5,7,11,13,17,19,23,29]
    assert len(t.obtener_pocion('datos_excel')) == 5
