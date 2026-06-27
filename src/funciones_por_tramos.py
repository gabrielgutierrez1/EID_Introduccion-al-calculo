from .utils import formatear_numero, son_iguales


def validar_digitos(digitos):
    if len(digitos) != 8:
        raise ValueError("Se requieren exactamente 8 digitos del cuerpo del RUT.")

    digitos_validados = []

    for digito in digitos:
        if isinstance(digito, str) and digito.isdigit():
            digito = int(digito)

        if not isinstance(digito, int) or digito < 0 or digito > 9:
            raise ValueError("Todos los digitos deben ser numeros enteros entre 0 y 9.")

        digitos_validados.append(digito)

    return digitos_validados


def seleccionar_caso(digitos):
    digitos = validar_digitos(digitos)
    d8 = digitos[7]
    resto = d8 % 3

    if resto == 0:
        return {
            "clave": "removible",
            "nombre": "Discontinuidad removible",
            "resto": resto,
            "regla": (
                f"Como d8 = {d8} es multiplo de 3, se genera el caso "
                "de discontinuidad removible."
            ),
        }

    if resto == 1:
        return {
            "clave": "salto",
            "nombre": "Discontinuidad de salto",
            "resto": resto,
            "regla": (
                f"Como d8 = {d8} deja residuo 1 al dividir por 3, se genera "
                "el caso de discontinuidad de salto."
            ),
        }

    return {
        "clave": "infinita",
        "nombre": "Discontinuidad infinita",
        "resto": resto,
        "regla": (
            f"Como d8 = {d8} deja residuo 2 al dividir por 3, se genera "
            "el caso de discontinuidad infinita."
        ),
    }


def construir_funcion_por_tramos(digitos):
    digitos = validar_digitos(digitos)
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    a = d3
    caso = seleccionar_caso(digitos)
    clave = caso["clave"]

    if clave == "removible":
        tramos = [
            {
                "condicion": f"x < {a}",
                "expresion": f"((x - {a})(x + {d1})) / (x - {a})",
            },
            {
                "condicion": f"x > {a}",
                "expresion": f"((x - {a})(x + {d1})) / (x - {a})",
            },
            {
                "condicion": f"x = {a}",
                "expresion": "no definida",
            },
        ]
        descripcion = (
            f"f(x) = ((x - {a})(x + {d1})) / (x - {a}), con x distinto de {a}"
        )
        simplificada = f"f(x) = x + {d1}, con x distinto de {a}"

    elif clave == "salto":
        tramos = [
            {
                "condicion": f"x < {a}",
                "expresion": f"x + {d2}",
            },
            {
                "condicion": f"x >= {a}",
                "expresion": f"x + {d4}",
            },
        ]
        descripcion = (
            "f(x) = { "
            f"x + {d2}, si x < {a}; "
            f"x + {d4}, si x >= {a} "
            "}"
        )
        simplificada = None

    else:
        numerador = d5 + 1
        tramos = [
            {
                "condicion": f"x < {a}",
                "expresion": f"{numerador} / (x - {a})",
            },
            {
                "condicion": f"x > {a}",
                "expresion": f"{numerador} / (x - {a})",
            },
            {
                "condicion": f"x = {a}",
                "expresion": "no definida",
            },
        ]
        descripcion = f"f(x) = {numerador} / (x - {a}), con x distinto de {a}"
        simplificada = None

    return {
        "digitos": digitos,
        "a": a,
        "caso": caso,
        "tramos": tramos,
        "descripcion": descripcion,
        "simplificada": simplificada,
    }


def evaluar_funcion(funcion, x):
    d1, d2, d3, d4, d5, d6, d7, d8 = funcion["digitos"]
    a = funcion["a"]
    clave = funcion["caso"]["clave"]

    if clave == "removible":
        if son_iguales(x, a):
            return None
        return ((x - a) * (x + d1)) / (x - a)

    if clave == "salto":
        if x < a:
            return x + d2
        return x + d4

    if son_iguales(x, a):
        return None

    return (d5 + 1) / (x - a)


def identificar_puntos_criticos(funcion):
    a = funcion["a"]
    clave = funcion["caso"]["clave"]
    motivos = [f"x = {a} es el punto donde se analiza la funcion, porque a = d3."]

    if clave == "salto":
        motivos.append("En este punto cambia el tramo de la funcion.")
    else:
        motivos.append(f"El denominador x - {a} se anula en x = {a}.")
        motivos.append("La funcion no esta definida en ese punto.")

    return [{"x": a, "motivos": motivos}]


def calcular_limites_laterales(funcion):
    d1, d2, d3, d4, d5, d6, d7, d8 = funcion["digitos"]
    a = funcion["a"]
    clave = funcion["caso"]["clave"]

    if clave == "removible":
        izquierda = a + d1
        derecha = a + d1
        return {
            "izquierda": izquierda,
            "derecha": derecha,
            "existe": True,
            "valor": izquierda,
            "pasos": [
                (
                    f"Se simplifica ((x - {a})(x + {d1})) / (x - {a}) "
                    f"= x + {d1}, siempre que x sea distinto de {a}."
                ),
                (
                    f"Limite por izquierda: {a} + {d1} = "
                    f"{formatear_numero(izquierda)}."
                ),
                (
                    f"Limite por derecha: {a} + {d1} = "
                    f"{formatear_numero(derecha)}."
                ),
            ],
        }

    if clave == "salto":
        izquierda = a + d2
        derecha = a + d4
        existe = son_iguales(izquierda, derecha)
        valor = izquierda if existe else None

        return {
            "izquierda": izquierda,
            "derecha": derecha,
            "existe": existe,
            "valor": valor,
            "pasos": [
                (
                    f"Para x < {a}, f(x) = x + {d2}; entonces el limite "
                    f"por izquierda es {a} + {d2} = {formatear_numero(izquierda)}."
                ),
                (
                    f"Para x >= {a}, f(x) = x + {d4}; entonces el limite "
                    f"por derecha es {a} + {d4} = {formatear_numero(derecha)}."
                ),
            ],
        }

    izquierda = "-infinito"
    derecha = "infinito"

    return {
        "izquierda": izquierda,
        "derecha": derecha,
        "existe": False,
        "valor": None,
        "pasos": [
            (
                f"El numerador d5 + 1 = {d5 + 1} es positivo y el denominador "
                f"x - {a} tiende a 0."
            ),
            (
                f"Por izquierda, x - {a} es negativo y muy pequeno; "
                "por eso la funcion tiende a -infinito."
            ),
            (
                f"Por derecha, x - {a} es positivo y muy pequeno; "
                "por eso la funcion tiende a infinito."
            ),
        ],
    }


def clasificar_continuidad(funcion, limites):
    a = funcion["a"]
    clave = funcion["caso"]["clave"]
    valor_en_a = evaluar_funcion(funcion, a)

    if limites["existe"] and valor_en_a is not None and son_iguales(valor_en_a, limites["valor"]):
        return {
            "es_continua": True,
            "valor_en_a": valor_en_a,
            "tipo_discontinuidad": "No hay discontinuidad",
            "justificacion": (
                f"El limite existe, f({a}) esta definida y ambos valores coinciden."
            ),
        }

    if clave == "removible":
        return {
            "es_continua": False,
            "valor_en_a": valor_en_a,
            "tipo_discontinuidad": "Discontinuidad removible",
            "justificacion": (
                f"El limite existe y vale {formatear_numero(limites['valor'])}, "
                f"pero f({a}) no esta definida porque el denominador se anula."
            ),
        }

    if clave == "salto" and not limites["existe"]:
        return {
            "es_continua": False,
            "valor_en_a": valor_en_a,
            "tipo_discontinuidad": "Discontinuidad de salto",
            "justificacion": (
                "Los limites laterales son finitos, pero no coinciden; "
                "por eso el limite bilateral no existe."
            ),
        }

    if clave == "infinita":
        return {
            "es_continua": False,
            "valor_en_a": valor_en_a,
            "tipo_discontinuidad": "Discontinuidad infinita",
            "justificacion": (
                f"La funcion no esta definida en x = {a} y los valores crecen "
                "sin limite cerca del punto. Hay una asintota vertical."
            ),
        }

    return {
        "es_continua": False,
        "valor_en_a": valor_en_a,
        "tipo_discontinuidad": "No clasificada",
        "justificacion": "No se cumplen las condiciones de continuidad en el punto.",
    }


def generar_tabla_valores(funcion):
    a = funcion["a"]
    desplazamientos = [-1, -0.1, -0.01, -0.001, 0.001, 0.01, 0.1, 1]
    tabla = []

    for desplazamiento in desplazamientos:
        x = a + desplazamiento
        valor = evaluar_funcion(funcion, x)
        lado = "izquierda" if desplazamiento < 0 else "derecha"

        tabla.append({
            "lado": lado,
            "desplazamiento": desplazamiento,
            "x": x,
            "x_texto": formatear_numero(x),
            "f_x": valor,
            "f_x_texto": formatear_numero(valor),
        })

    return tabla


def generar_puntos_grafico(funcion, inicio=None, fin=None, cantidad_por_lado=80, limite_y=100):
    a = funcion["a"]

    if inicio is None:
        inicio = a - 5

    if fin is None:
        fin = a + 5

    if cantidad_por_lado < 2:
        cantidad_por_lado = 2

    segmentos = []
    rangos = [(inicio, a - 0.001), (a + 0.001, fin)]

    for x_inicial, x_final in rangos:
        paso = (x_final - x_inicial) / (cantidad_por_lado - 1)
        puntos = []
        i = 0

        while i < cantidad_por_lado:
            x = x_inicial + paso * i
            y = evaluar_funcion(funcion, x)

            if y is not None and -limite_y <= y <= limite_y:
                puntos.append({"x": x, "y": y})

            i += 1

        segmentos.append(puntos)

    return segmentos


def obtener_campos_defensa():
    return [
        {"clave": "limite_izquierda", "etiqueta": "Limite por la izquierda", "valor": ""},
        {"clave": "limite_derecha", "etiqueta": "Limite por la derecha", "valor": ""},
        {"clave": "existe_limite", "etiqueta": "Conclusion sobre el limite", "valor": ""},
        {"clave": "valor_funcion", "etiqueta": "Valor de la funcion en el punto", "valor": ""},
        {"clave": "continuidad", "etiqueta": "Conclusion sobre continuidad", "valor": ""},
        {"clave": "tipo_discontinuidad", "etiqueta": "Tipo de discontinuidad", "valor": ""},
        {"clave": "justificacion", "etiqueta": "Justificacion escrita", "valor": ""},
    ]


def construir_pasos(funcion, puntos_criticos, limites, continuidad):
    a = funcion["a"]
    pasos = [
        f"Se define el punto principal de analisis como a = d3 = {a}.",
        funcion["caso"]["regla"],
        f"Funcion generada: {funcion['descripcion']}",
    ]

    if funcion["simplificada"]:
        pasos.append(f"Simplificacion manual: {funcion['simplificada']}")

    for punto in puntos_criticos:
        for motivo in punto["motivos"]:
            pasos.append(motivo)

    pasos.extend(limites["pasos"])

    if limites["existe"]:
        pasos.append(
            "Como los limites laterales coinciden, el limite bilateral existe "
            f"y vale {formatear_numero(limites['valor'])}."
        )
    else:
        pasos.append("Como los limites laterales no coinciden como numero real, el limite bilateral no existe.")

    pasos.append(
        f"Valor de la funcion en el punto: f({a}) = "
        f"{formatear_numero(continuidad['valor_en_a'])}."
    )
    pasos.append(continuidad["justificacion"])
    pasos.append(f"Conclusion: {continuidad['tipo_discontinuidad']}.")

    return pasos


def analizar_funcion_por_tramos(digitos):
    funcion = construir_funcion_por_tramos(digitos)
    puntos_criticos = identificar_puntos_criticos(funcion)
    limites = calcular_limites_laterales(funcion)
    continuidad = clasificar_continuidad(funcion, limites)
    tabla = generar_tabla_valores(funcion)
    campos_defensa = obtener_campos_defensa()
    puntos_grafico = generar_puntos_grafico(funcion)
    pasos = construir_pasos(funcion, puntos_criticos, limites, continuidad)

    return {
        "funcion": funcion,
        "a": funcion["a"],
        "caso": funcion["caso"],
        "puntos_criticos": puntos_criticos,
        "limites": limites,
        "continuidad": continuidad,
        "tabla": tabla,
        "campos_defensa": campos_defensa,
        "puntos_grafico": puntos_grafico,
        "pasos": pasos,
    }

