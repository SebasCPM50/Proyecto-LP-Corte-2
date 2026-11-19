datos = invocar desde "datos/inventario.csv";
disponibles = purificar datos donde (stock > 0 y precio < 100) o categoria == "oferta";
agotados_no_ofertados = purificar datos donde stock == 0 y no categoria == "oferta";
